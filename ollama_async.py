import os
import asyncio
from ollama import AsyncClient
from dotenv import load_dotenv


async def chat():
  load_dotenv()
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  response = await AsyncClient(host="https://ollama.com",headers={'Authorization': os.getenv('OLLAMA_TOKEN')}).chat(model='gpt-oss:120b', messages=[message])

asyncio.run(chat()) 