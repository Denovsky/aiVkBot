import os
import sys
from ollama_logic import Ollama_chat
import promts
import tg_messages_handler

chat = Ollama_chat()
messages_filepath = "messages/"
listfiles = os.listdir(messages_filepath)

def createChat():
    print("Creating new chat.")
    chat.sendMessage(promts.message2)
    response = chat.getResponse()

def restoreChat():
    if len(listfiles) == 0:
        print("Nothing to load.")
        createChat()
    elif len(listfiles) == 1:
        chat.loadHistory(messages_filepath + listfiles[0])
    else:
        while(1):
            print("Choose your file:")
            for elem in listfiles:
                print(f"\t - {elem}")
            inp = input("Enter filename: ")
            if inp in listfiles:
                chat.loadHistory(messages_filepath + inp)
                break
            print("Please, try again.")

def readArgs():
    if len(sys.argv) > 1:
        if sys.argv[1] == "new":
            createChat()
            return None
    restoreChat()
    return None

readArgs()
chat.displayHistory()

"""
Цикл отправки сообщения
data = input("Question: ")
chat.sendMessage(data)
response = chat.getResponse()
print(f"\nResponse: {response}\n")
"""

# data = tg_messages_handler.messages_history
# chat.sendMessage(data)
# response = chat.getResponse()
# print(f"\nResponse: {response}\n")

try:
    while (1):
        data = input("Question: ")
        if data == "undo":
            chat.deleteStage()
            chat.displayHistory()
            continue
        chat.sendMessage(data)
        response = chat.getResponse()
        print(f"\nResponse: {response}\n")
except KeyboardInterrupt as k_e:
    print(f"KeyboardInterrupt: {k_e}")
    isSave = input("Do you need to save chat history? (y or n): ")
    if isSave == 'y' or isSave == 'н':
        filename = input("Input file name: ")
        chat.saveHistory(messages_filepath + filename + ".json")
    else:
        isSave = input("You REALLY need to save chat history? (y or n): ")
        if isSave == 'y' or isSave == 'н':
            filename = input("Input file name: ")
            chat.saveHistory(messages_filepath + filename + ".json")
        else:
            print("OK. Done.")
except Exception as e:
    print(f"Other exception: {e}")
    chat.saveHistory(messages_filepath + "error_file_itnterruption.json")
