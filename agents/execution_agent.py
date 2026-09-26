from langchain_groq import ChatGroq
from tools.complex_calculation import tools
from langchain_core.messages import SystemMessage, HumanMessage
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

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)

execution_agent = model.bind_tools(tools)

def execution_agent_node(state: State):
    context = f"""
            User query: {state.get('user_query')}
        
            Gathered so far:
        
            - Web search result: {state.get('web_search_result') or 'none yet'}
            - Execution result: {state.get('execution_result') or 'none yet'}
            """
    print("[INFO] Execution agent thinking...")
    messages = [
        SystemMessage(content=EXECUTION_AGENT_PROMPT),
        HumanMessage(content=context),
    ]
    response = execution_agent.invoke(messages)
    print("[INFO] Execution agent sending response to coordinator agent")
    print(response)
    update = {"messages": [response]}
    if not response.tool_calls and response.content:
        update["execution_result"] = response.content
    return update