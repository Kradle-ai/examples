from kradle.models import ChallengeInfo, Observation, InitParticipantResponse, OnEventResponse
from kradle.api.client import KradleAPI
from kradle.logger import KradleLogger
import time

class AgentManagerMock:
    """
    A mock version of the AgentManager that removes server and network components.
    This allows for direct testing of agents by passing data as parameters.
    """

    def __init__(self, agent_class):
        self.agent_class = agent_class
        self.agent = None
        self._api_client = KradleAPI()
        self._logger = KradleLogger()

    def init_agent(self, data) -> InitParticipantResponse:
        """
        Create an agent with initdata
        
        Args:
            data (dict): Dictionary containing event data including:
                - participantId: ID of the participant
                - runId: ID of the run
                - task: Task to be performed
                - agent_modes: Modes of the agent
                - js_functions: JavaScript functions to be used
                - available_events: Events to be listened to
                
        Returns:
            The response from the agent's init_participant method
        """
        required_fields = ["participantId", "runId", "task", "agent_modes", "js_functions", "available_events"]
        for field in required_fields:
            if data.get(field) is None:
                raise ValueError(f"{field} is required in the init data")
            
        if (self.agent is not None):
            raise ValueError("Agent already initialized")
        
        # Create the agent instance
        self.agent = self.agent_class(
            api_client=self._api_client,
            participant_id=data.get("participantId"),
            run_id=data.get("runId")
        )

        challenge_info = ChallengeInfo(
            participant_id=data.get("participantId"),
            run_id=data.get("runId"),
            task=data.get("task"),
            agent_modes=data.get("agent_modes"),
            js_functions=data.get("js_functions"),
            available_events=data.get("available_events"),
        )

        self.agent.log = lambda message: print(f"Agent log: {str(message)[:60]+" <truncated>..." if message is not None else ''}")

        try:
            # Initialize the agent
            init_response = self.agent.init_participant(challenge_info)
            print(init_response)
            #print(f"Agent initialized with events: {init_response.listenTo}")

            return init_response
        except ValueError as e:
            print(f"Failed to initialize agent: {str(e)}")

    def handle_event(self, data) -> OnEventResponse:
        """
        Handle an event for an agent.
        
        Args:
            data (dict): Dictionary containing event data including:
                - participantId: ID of the participant
                - runId: ID of the run
                - event: Event type
                - and other event-specific data
            username (str, optional): Username of the agent to handle the event

        See sample_data.py for sample event data or https://app.kradle.ai/docs/how-kradle-works
            
        Returns:
            The response from the agent's on_event method
        """
        required_fields = ["name", "event", "observationId", "participantId", "executing", "chat_messages", "position", "health", "health_status", "weather", "time", "inventory", "blocks", "players", "entities", "craftable"]
        for field in required_fields:
            if data.get(field) is None:
                raise ValueError(f"{field} is required in the event data for the observation")
            
        participant_id = data.get("participantId")

        observation = Observation.from_event(data)
        try:
            start_time = time.time()
            result = self.agent.on_event(observation)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Event handling time: {execution_time:.4f} seconds")
            return result
        except ValueError as e:
            print(f"Error in event handler for participant {participant_id}", e)
            raise e
