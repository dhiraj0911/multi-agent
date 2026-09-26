from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import State

SYNTHESIS_AGENT_PROMPT = """
You are an Synthesis Agent in a multi-agent system.

Your responsibility is to synthesize information from multiple agents and provide a coherent summary.
"""

synthesis_agent = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)

def synthesis_agent_node(state: State):
    context = f"""
        User query: {state.get('user_query')}
    
        Gathered so far:
    
        - Web search result: {state.get('web_search_result') or 'none yet'}
        - Execution result: {state.get('execution_result') or 'none yet'}
        """
    print("[INFO] Synthesis agent thinking...")
    messages = [
        SystemMessage(content=SYNTHESIS_AGENT_PROMPT),
        HumanMessage(content=context),
    ]
    response = synthesis_agent.invoke(messages)
    print("[INFO] Synthesis agent summarizing gathered information")
    return {
        "final_result": response.content,
        "is_completed": True,
        "messages": [response],
    }