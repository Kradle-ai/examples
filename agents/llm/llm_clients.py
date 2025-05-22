import json
import os
import threading
from typing import Any, Protocol, cast, Optional

import requests
from kradle import JSON_RESPONSE_FORMAT, KradleAPI


class LLMError(Exception):
    def __init__(self, message: str, details: Optional[str] = None, content: Optional[str] = None):
        super().__init__(message)
        self.details = details
        self.content = content

    def message_with_details(self) -> str:
        if self.details:
            return f"{str(self)}: {self.details}"
        else:
            return str(self)


class LLMResponse:
    def __init__(self, content: str, raw_response: dict[str, Any]):
        self.content = content
        self.raw_response = raw_response


class LLMClient(Protocol):
    def get_chat_completion(
        self,
        messages: list[dict[str, str]],
    ) -> LLMResponse:
        """Returns the message content from the LLM response.

        Args:
            model: The model to use for the LLM.
            messages: The messages to send to the LLM.

        Returns:
            The message content from the LLM response. Different servers may
            return a different envelope, so this returns the provider-specific
            actual model response.
        """
        ...


class OpenRouterClient(LLMClient):
    def __init__(self, model: str, api: KradleAPI):
        self._model = model

        # Look for OpenRouter API key in environment variables, falling back to
        # Kradle API if not found.
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key is None or len(api_key) < 20:
            human = api.humans.get()
            api_key = cast(Optional[str], human["openRouterKey"])
        if api_key is None:
            raise LLMError("OPENROUTER_API_KEY is not set")
        self._api_key: str = api_key

    def get_chat_completion(
        self,
        messages: list[dict[str, str]],
    ) -> LLMResponse:
        request = {
            "model": self._model,
            "messages": messages,
            "require_parameters": True,
            "response_format": JSON_RESPONSE_FORMAT,
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self._api_key}"},
            json=request,
            timeout=30,
        ).json()

        if "choices" not in response or not response["choices"]:
            raise LLMError(
                "Cannot parse response from LLM",
                f"Full response: {response}",
            )

        return LLMResponse(
            content=cast(str, response["choices"][0]["message"]["content"]),
            raw_response=response,
        )


class OllamaClient:
    def __init__(self, model: str):
        self._model = model

        url = os.getenv("OLLAMA_API_URL")
        if url is None:
            raise LLMError("OLLAMA_API_URL is not set")
        self._url = url

    def get_chat_completion(
        self,
        messages: list[dict[str, str]],
    ) -> LLMResponse:
        schema = cast(Any, JSON_RESPONSE_FORMAT)["json_schema"]["schema"]
        request = {
            "model": self._model,
            "messages": messages,
            "format": schema,
            "stream": False,
            "keep_alive": -1  # prevent model from timing out of cache,
        }

        response = requests.post(
            self._url,
            json=request,
            timeout=30,
        ).json()

        if "message" not in response:
            raise LLMError(
                "Cannot parse response from Ollama",
                f"Full response: {response}",
            )

        return LLMResponse(
            content=cast(str, response["message"]["content"]),
            raw_response=response,
        )


class WaitingClient:
    def __init__(self, delegate: LLMClient):
        self._delegate = delegate
        self._lock = threading.Lock()

    def get_chat_completion(
        self,
        messages: list[dict[str, str]],
    ) -> LLMResponse:
        if not self._lock.acquire(blocking=False):
            print("Already waiting for LLM response, skipping new request")
            return LLMResponse("""{
                "code": "",
                "message": "Ignoring event, I'm already busy thinking",
            }""",
            {},
        )

        try:
            return self._delegate.get_chat_completion(messages)
        finally:
            self._lock.release()


def parse_action_from_response(response: LLMResponse) -> dict[str, Any]:
    content = response.content
    if not content:
        raise LLMError(
            "Unable to extract content from LLM response",
            f"Full response: {response.raw_response}",
            content,
        )

    # Find the JSON part in the content
    start = content.find("{")
    end = content.rfind("}") + 1
    content_to_parse = content[start:end]
    if not content_to_parse:
        raise LLMError(
            "Unable to parse JSON from LLM response",
            f"Received: {content}",
            content
        )

    # Parse the content string as JSON and extract the code and message
    try:
        json_content = json.loads(content_to_parse)
        action = {
            "code": json_content.get("code", ""),
            "message": json_content.get("message", "")
        }
        return action

    except Exception as e:
        raise LLMError(
            "Unable to parse JSON from LLM response",
            f"Unable to parse JSON from LLM response for content: {content_to_parse} with error: {e}",
            content
        ) from e
