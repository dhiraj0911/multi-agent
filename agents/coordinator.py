from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graph.state import State
from model.schema import RouteDecision

# - rag: retrieves internal/knowledge-base context
COORDINATOR_AGENT_PROMPT = """
You are a Coordinator Agent in a multi-agent system.

Your job is to look at the conversation so far and the results
gathered (RAG, web search, execution) and decide what happens next.

Available agents:
- web_search: searches the web for external/current info
- execution: runs code or performs an action
- synthesis: combines all gathered results into a final answer
- end: use only if synthesis has already produced the final_result

Rules:
- Only route to an agent if its result is still missing or insufficient.
- Do not call the same agent twice unless its previous result was empty or irrelevant.
- Once web_search/execution results are sufficient, route to "synthesis".
- Be decisive — always pick exactly one next_agent.
"""

coordinator_model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
).with_structured_output(RouteDecision)

def coordinator_agent_node(state: State):
    # - RAG result: {state.get('rag_result') or 'none yet'}
    context = f"""
    User query: {state.get('user_query')}

    Gathered so far:

    - Web search result: {state.get('web_search_result') or 'none yet'}
    - Execution result: {state.get('execution_result') or 'none yet'}
    """

    messages = [
        SystemMessage(content=COORDINATOR_AGENT_PROMPT),
        HumanMessage(content=context),
    ]
    print("[INFO] Coordinator agent thinking...")
    response = coordinator_model.invoke(messages)
    print(f"[INFO] Coordinator agent decided to route to {response.next_agent} because {response.reasoning}")
    return {
        "messages": [AIMessage(content=f"Routing to {response.next_agent}: {response.reasoning}", name="coordinator")],
        "next_agent": response.next_agent,
        "is_completed": response.is_completed,
    }