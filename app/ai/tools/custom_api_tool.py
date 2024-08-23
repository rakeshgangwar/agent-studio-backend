import string
from typing import Dict, Any, Optional
from langchain.tools import BaseTool
import requests
from pydantic import Field


class CustomAPITool(BaseTool):
    name: str = "Custom API Tool"
    description: str = "A configurable tool for making API calls"
    api_config: Dict[str, Any] = Field(..., description="Configuration for the API")

    def _run(self, query: str) -> str:
        """Execute the API call"""
        method = self.api_config.get('method', 'GET').upper()
        url = self.api_config['url']
        headers = self.api_config.get('headers', {})
        params = self.api_config.get('params', {})
        data = self.api_config.get('data', {})

        # Perform parameter substitution
        url = self._substitute_params(url, query)
        params = {k: self._substitute_params(v, query) for k, v in params.items()}

        # Remove any quotes from parameter values
        params = {k: v.strip("'\"") for k, v in params.items()}

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"API call failed: {str(e)}"

    def _substitute_params(self, text: str, query: str) -> str:
        """Substitute placeholders in the text with values from the query"""
        template = string.Template(text)
        return template.safe_substitute(query=query)

    async def _arun(self, query: str) -> str:
        """Asynchronous execution of the API call"""
        return self._run(query)


# Example usage:
def create_api_tool(api_config: Dict[str, Any]) -> CustomAPITool:
    return CustomAPITool(api_config=api_config)


weather_api_config = {
    'url': 'https://api.openweathermap.org/data/2.5/weather',
    'method': 'GET',
    'params': {
        'q': '$query',
        'appid': '272fcb70d2c4e6f5134c2dce7d091df6',
        'units': 'metric'
    }
}

weather_tool = create_api_tool(weather_api_config)

from langchain.agents import initialize_agent, Tool
from langchain_openai import OpenAI

tools = [
    Tool(
        name="Weather Information",
        func=weather_tool.run,
        description="Get weather information for a city. Input should be a city name."
    )
]

llm = OpenAI(temperature=0, api_key="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")
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Example agent execution
result = agent.invoke(input="What's the weather like in London?")
print(result)
