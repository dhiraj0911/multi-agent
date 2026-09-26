from langchain.chat_models import init_chat_model
from tools.search_tool import tools
from langchain_core.messages import SystemMessage
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

model = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="groq",
    temperature=0.7
)

web_search_agent = model.bind_tools(tools)

def web_search_agent_node(state: State):
    messages = [SystemMessage(content=WEB_SEARCH_PROMPT)] + state["messages"]
    response = web_search_agent.invoke(messages)
    return {
        "message": response
    }