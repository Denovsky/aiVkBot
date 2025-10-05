from ollama_logic import Ollama_chat

chat = Ollama_chat()
while (1):
    data = input("Question: ")
    chat.sendMessage(data)
    response = chat.getResponse()
    print(f"\nResponse: {response}\n")

