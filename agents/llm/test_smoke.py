# test if the LLM agent is able to respond with json to a simple init and event prompt

from agent_manager_mock import AgentManagerMock
from base_llm_agent import BaseLLMAgent
from llm_agent import create_llm_agent_class
from samples.sample_data import SAMPLE_INIT_DATA, SAMPLE_EVENT_INITIAL_STATE, SAMPLE_EVENT_COMMAND_EXECUTED_ERROR

def test_code_contains_await(event, event_name):
    if event['code'] and 'await' in event['code']:
        print(f"✅ Test passed: {event_name}['code'] contains 'await'")
    else:
        print(f"❌ Test failed: {event_name}['code'] does not contain 'await'")

# agent_class = create_llm_agent_class({ "model":"qwen2.5-coder:7b"})
agent_class = BaseLLMAgent

agent_test_manager = AgentManagerMock(agent_class)

print("================================================")
agent_test_manager.init_agent(SAMPLE_INIT_DATA)

event1 = agent_test_manager.handle_event(SAMPLE_EVENT_INITIAL_STATE)
# Test event1
test_code_contains_await(event1, "event1")

event2 = agent_test_manager.handle_event(SAMPLE_EVENT_COMMAND_EXECUTED_ERROR)
# Test event2
test_code_contains_await(event2, "event2")

print("================================================") 
