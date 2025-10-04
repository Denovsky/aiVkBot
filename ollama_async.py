import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  response = await AsyncClient(host="https://ollama.com",headers={'Authorization': 'a64be015a40246dc983de3e4b0fe852e.fUE1BNcoRPbRNmGFHIygICpe'}).chat(model='gpt-oss:120b', messages=[message])

asyncio.run(chat()) 