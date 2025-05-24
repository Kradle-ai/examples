import json
import os
import textwrap
import threading
from typing import Any, Protocol, cast, Optional

import requests
from kradle import JSON_RESPONSE_FORMAT, KradleAPI, OnEventResponse


class LLMError(Exception):
    """An error that occurs when interacting with an LLM."""

    def __init__(self, message: str, details: Optional[str] = None, content: Optional[str] = None):
        super().__init__(message)
        self.details = details
        self.content = content


def message_with_details(error: Exception) -> str:
    """Returns a string representation of an error, including details if available."""
    if isinstance(error, LLMError) and error.details:
        return f"{str(error)}: {error.details}"
    else:
        return str(error)


class LLMResponse:
    """The response from an LLM.

    This includes the unparsed message content from the LLM in the `content`
    property, and the raw JSON response from the LLM API. The raw response will
    vary based on the LLM API provider.
    """

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
            messages: The messages to send to the LLM.

        Returns:
            The message content from the LLM response. Different servers may
            return a different envelope, so this returns the provider-specific
            actual model response.
        """
        ...


class OpenRouterClient(LLMClient):
    """An LLM client that uses the OpenRouter API."""

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
    """An LLM client that uses the Ollama API."""

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
            "keep_alive": -1,  # prevent model from timing out of cache,
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
    """An LLM client that you can overlay on top of another `LLMClient` to
    prevent interruptions while waiting for a response.

    This is useful if you want to use a slow LLM that might take a while to
    respond, and you don't want to overwhelm the LLM with requests while it's
    thinking.
    """

    def __init__(self, delegate: LLMClient):
        self._delegate = delegate
        self._lock = threading.Lock()

    def get_chat_completion(
        self,
        messages: list[dict[str, str]],
    ) -> LLMResponse:
        if not self._lock.acquire(blocking=False):
            print("Already waiting for LLM response, skipping new request")
            return LLMResponse(
                textwrap.dedent("""
                {
                    "code": "",
                    "message": "Ignoring event, I'm already busy thinking",
                }"""),
                {},
            )

        try:
            return self._delegate.get_chat_completion(messages)
        finally:
            self._lock.release()


def parse_action_from_response(response: LLMResponse) -> OnEventResponse:
    """Parses the content from an LLM response into an `OnEventResponse` object.

    This is a helper function that attempts to extract the `code` and `message`
    from the LLM response. If the content is not valid JSON, it raises an
    `LLMError`.
    """
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
        raise LLMError("Unable to parse JSON from LLM response", f"Received: {content}", content)

    # Parse the content string as JSON and extract the code and message
    try:
        json_content = json.loads(content_to_parse)
        action = OnEventResponse(
            code=json_content.get("code", ""),
            message=json_content.get("message", ""),
        )
        return action

    except Exception as e:
        raise LLMError(
            "Unable to parse JSON from LLM response",
            f"Unable to parse JSON from LLM response for content: {content_to_parse} with error: {e}",
            content,
        ) from e
