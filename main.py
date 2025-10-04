from ollama_logic import Ollama_chat

chat = Ollama_chat()
chat.sendMassage('Did you remember rules?')
print(chat.getResponse())

