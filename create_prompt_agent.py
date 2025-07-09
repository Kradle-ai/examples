from kradle import Kradle

from dotenv import load_dotenv

load_dotenv()

kradle = Kradle(create_public_url=True, debug=True)

username = "test1243"
data = {
    "name": "test234",
    "prompt_config": {
        "model": "openai/gpt-4o",
        "persona": "you are a helpful assistant!",
        "respond_with_code": False,  # we need this for now or the API throws an error
    },
    "description": "test2",
    "visibility": "private",
}

try:
    kradle._api_client.agents.create(username, **data)
    print("Agent created successfully")
except Exception as e:
    print(e)

    try:
        kradle._api_client.agents.update(username, **data)
        print("Agent updated successfully")

    except Exception as e:
        print(e)
        print("Agent update failed")
