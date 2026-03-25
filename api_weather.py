import requests

def get_weather(city, api):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"

    response = requests.get(url)

    if response.status_code == 401:
        return {"error": "Invalid API"}

    data = response.json()
    return data["main"]["temp"]


# ассинхрон
import aiohttp
import asyncio

async def get_weather_async(city, api):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.json()
            return data["main"]["temp"]