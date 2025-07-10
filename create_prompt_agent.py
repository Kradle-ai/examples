from kradle import Kradle

from dotenv import load_dotenv

"""
An example of creating and updating a prompt agent.
"""

load_dotenv()

kradle = Kradle(debug=True)

username = "test1234"
data = {
    "username": username,
    "name": username,
    "prompt_config": {
        "model": "openai/gpt-4o",
        "persona": "you are a super duper helpful assistant!",
        "respond_with_code": False,  # we need this for now or the API throws an error
    },
    "description": "test2",
    "visibility": "private",
}

try:
    kradle._api_client.agents.create(**data)
    print("Agent created successfully")
except Exception as e:
    print(e)

    try:
        kradle._api_client.agents.update(**data)
        print("Agent updated successfully")

    except Exception as e:
        print(e)
        print("Agent update failed")
