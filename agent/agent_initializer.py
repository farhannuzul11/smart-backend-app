# agent/agent_initializer.py
from langchain.agents import initialize_agent, AgentType

def create_agent(llm, tools):
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # Choose the agent's problem-solving style with reasoning and tool use based on tool descriptions.
        verbose=True, # 	Enable detailed logging of the agent's thoughts and actions for easier debugging and insight.
        handle_parsing_errors=True
    )
