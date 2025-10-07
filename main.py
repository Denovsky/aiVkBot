import os
import sys
import json
from ollama_logic import Ollama_chat

chat = Ollama_chat()
history_filepath = "history.json"
if len(sys.argv) > 1:
    chat_state_arg = sys.argv[1]
    if chat_state_arg != "new":
        chat.loadHistory(history_filepath)
        chat.displayHistory()
    else:
        chat.initMessage()
        response = chat.getResponse()
        print(f"\nResponse: {response}\n")
else:
    chat.loadHistory(history_filepath)
    chat.displayHistory()
    # chat.saveResponseIntoFile("psql_script.py", 3)


# data = "В следующих 10 сообщения я отправлю тебе код каждого из 10 файлов. Твоя задача расписать модель взаимодействии этих файлов и какой файл за что отвечает. Ты готов?"
# chat.sendMessage(data)
# response = chat.getResponse()
# print(f"\nResponse: {response}\n")

# path = "../yahboom_backup_software/MutoLib/MutoLib"
# for filename in os.listdir(path):
#     try:
#         with open(f"{path}/{filename}", 'r', encoding='utf-8') as f:
#             data = f.read()
#             chat.sendMessage(f"{filename}: {data}")
#             response = chat.getResponse()
#             print(f"\nResponse: {response}\n")
#     except Exception as e:
#         print(f"Reading error: {e}")
# try:
#     while (1):
#         data = input("Question: ")
#         chat.sendMessage(data)
#         response = chat.getResponse()
#         print(f"\nResponse: {response}\n")
# except KeyboardInterrupt as k_e:
#     print(f"KeyboardInterrupt: {k_e}")
#     chat.saveHistory(history_filepath)
# except Exception as e:
#     print(f"Other exception: {e}")
