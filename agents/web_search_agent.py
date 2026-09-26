from langchain_groq import ChatGroq
from tools.search_tool import tools
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graph.state import State

WEB_SEARCH_PROMPT = """
You are a Web Search Agent in a multi-agent system.

Your responsibility is to find accurate and relevant
information from the web.

Rules:
- Use the web search tool when external information is required.
- Formulate an effective search query.
- Do not fabricate search results.
- Prefer relevant and recent information when appropriate.
- Return the useful information found from the search.
- You are not responsible for final answer generation.
"""

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)

web_search_agent = model.bind_tools(tools)

def web_search_agent_node(state: State):
    context = f"""
        User query: {state.get('user_query')}
    
        Gathered so far:
    
        - Web search result: {state.get('web_search_result') or 'none yet'}
        - Execution result: {state.get('execution_result') or 'none yet'}
        """
    print("[INFO] Web search agent searching...")
    messages = [
        SystemMessage(content=WEB_SEARCH_PROMPT),
        HumanMessage(content=context),
    ]
    response = web_search_agent.invoke(messages)
    print("[INFO] Web search agent obtained search results and sending update to coordinator agent")
    update = {"messages": [response]}
    if not response.tool_calls and response.content:
        update["web_search_result"] = response.content
    return update