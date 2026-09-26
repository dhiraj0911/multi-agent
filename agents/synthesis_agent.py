from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from graph.state import State

SYNTHESIS_AGENT_PROMPT = """
You are an Synthesis Agent in a multi-agent system.

Your responsibility is to synthesize information from multiple agents and provide a coherent summary.
"""

synthesis_agent = init_chat_model(
    model="gpt-4",
    model_provider="openai",
    temperature=0.7
)

def synthesis_agent_node(state: State):
    messages = [SystemMessage(content=SYNTHESIS_AGENT_PROMPT)] + state["messages"]
    response = synthesis_agent.invoke(messages)
    return {
        "message": response
    }