import json
import os
from ollama import Client
from config import OLLAMA_TOKEN
import promts # Содержит начальные сообщение
# import messages_new2


class Ollama_chat():

    # Натуральные и товарные хозяйстав
    # Товар и его своейства
    # Деньги и их функции
    def __init__(self):
        self.host = "https://ollama.com"
        self.token = OLLAMA_TOKEN
        self.model = "deepseek-v3.1:671b"
        # self.model = "kimi-k2:1t-cloud"
        self.user_role = "user"
        self.assistant_role = "assistant"
        self.question = ""
        self.response = ""
        self.messages_history = []

        self.initChat()

    def initChat(self):
        self.client = Client(
            host=self.host,
            headers={"Authorization": self.token}
        )

    def sendMessage(self, content, role="user"): # добавляет сообщение в историю сообщений
        self.question = content
        self.messages_history.append(self.formatMessage(content, role))
        
    def getResponse(self): # получает ответ и добавляет в историю
        self.response = self.client.chat(self.model, messages=self.messages_history)
        self.sendMessage(self.response.message.content, self.assistant_role)
        return self.response.message.content

    def formatMessage(self, content, role):
        if content == '' or role == '':
            return None
        return { "role": role, "content": content }     
    
    def deleteStage(self):
        del self.messages_history[-1] # delete response
        del self.messages_history[-1] # delete question

    def getClient(self):
        return self.client
    
    def getHistory(self):
        return self.messages_history
    
    def saveHistory(self, filepath):
        try:
            with open(filepath, "w") as json_file:
                json.dump(self.messages_history, json_file, indent=4)
            print("History has been successfully saved")
        except Exception as e:
            print(f"Save error: {e}")

    def loadHistory(self, filepath):
        try:
            with open(filepath, 'r') as file:
                self.messages_history = json.load(file)
            print("History has been successfully loaded")
        except Exception as e:
            print(f"Load error: {e}")

    def clearHistory(self, filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Delete error: {e}")

    def displayHistory(self):
        for elem in self.messages_history:
            if elem["role"] == self.assistant_role:
                print("="*20)
                print(elem["content"])

    def saveResponseIntoFile(self, filename, index):
        try:
            with open(filename, 'w') as file:
                file.write(self.messages_history[index]["content"])
            print("Script has been saved")
        except Exception as e:
            print(e)

    # def restoreHistory(self): # using after except. Using for unexpected interuptions
    #     for i in range(len(messages_new2.messages)):
    #         if i % 2 == 0:
    #             message = {
    #                 "role": self.user_role,
    #                 "content": messages_new2.messages[i]
    #             }
    #             self.messages_history.append(message)
    #         else:
    #             message = {
    #                 "role": self.assistant_role,
    #                 "content": messages_new2.messages[i]
    #             }
    #             self.messages_history.append(message)