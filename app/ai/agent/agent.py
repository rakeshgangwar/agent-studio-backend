# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229")
# search = TavilySearchResults(max_results=2)
tools = []
agent_executor = create_react_agent(model, tools, checkpointer=memory)


def create_re_agent(model, tools, prompt, memory):
    return create_react_agent(model, tools, checkpointer=memory)

