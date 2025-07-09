from kradle import Kradle

from kradle.api.resources.agent import AgentType, PromptConfig

from dotenv import load_dotenv

load_dotenv()

kradle = Kradle(create_public_url=True, debug=True)

username = "test1243"
data = {
    "name": "test234",
    "type": AgentType.PROMPT,
    "config": PromptConfig(
        model="openai/gpt-4o",
        persona="test it baby",
    ),
    "description": "test2",
}

try:
    kradle._api_client.agents.create(
        username,
        **data
    )
    print("Agent created successfully")
except Exception as e:
    print(e)
 
    try:
        kradle._api_client.agents.update(
            "test1243",
            **data
        )
        print("Agent updated successfully")

    except Exception as e:
        print(e)
        print("Agent update failed")        




