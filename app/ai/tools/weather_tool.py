import os
from typing import Any

import requests
from langchain.tools import BaseTool
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()


class WeatherTool(BaseTool):
    name = "weather"
    description = ("This tool is used to obtain weather forecast information. You need to enter the English city name. "
                   "The parameter format is: Lucknow")

    def __init__(self):
        super().__init__()

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def _run(self, para: str) -> str:
        try:
            if not para:
                return "Parameter cannot be empty"
            encoded_city = quote(para)

            openweather_appid = os.getenv("OPENWEATHER_APPID")

            api_url = (f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid"
                       f"={openweather_appid}")

            response = requests.get(api_url)
            if response.status_code == 200:
                weather_data = response.json()

                temperature_kelvin = weather_data['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15
                feels_like_kelvin = weather_data['main']['feels_like']
                feels_like_celsius = feels_like_kelvin - 273.15
                humidity = weather_data['main']['humidity']
                description = weather_data['weather'][0]['description']
                wind_speed = weather_data['wind']['speed']

                weather_description = (f"Today's weather：{description}，Current Temperature：{temperature_celsius:.2f} "
                                       f"degree celsius, Feels Like Temperature：{feels_like_celsius:.2f} degree "
                                       f"celsius, Wind Speed：{wind_speed} m/s, Humidity：{humidity}%")

                return f"Weather information for {encoded_city}：\n{weather_description}"
            else:
                return f"Failed to obtain weather information. Response status code: {response.status_code}"
        except Exception as e:
            return f"Error：{str(e)}"


if __name__ == "__main__":
    weather_tool = WeatherTool()
    weather_info = weather_tool.run("Lucknow")
    print(weather_info)
