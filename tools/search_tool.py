from langchain_tavily import TavilySearch

# TAVILY_API_KEY is expected to be set in the env
search_tool = TavilySearch(
    max_results=5
)

tools = [search_tool]