from langchain.chat_models import init_chat_model
from tools.complex_calculation import tools
from langchain_core.messages import SystemMessage
from graph.state import State

EXECUTION_AGENT_PROMPT = """
You are an Execution Agent in a multi-agent system.

Your responsibility is to execute computational and
operational tasks using the tools available to you.

- Analyze the assigned task.
- Select the appropriate tool.
- Never fabricate execution results.
- Return concise and accurate results.
- Do not perform tasks outside your responsibility.
"""

model = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="groq",
    temperature=0.7
)

execution_agent = model.bind_tools(tools)

def execution_agent_node(state: State):
    messages = [SystemMessage(content=EXECUTION_AGENT_PROMPT)] + state["messages"]
    response = execution_agent.invoke(messages)
    return {
        "message": response
    }