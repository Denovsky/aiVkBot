import json
import os
from ollama import Client
from config import OLLAMA_TOKEN


class Ollama_chat():
    def __init__(self):
        self.host = "https://ollama.com"
        self.token = OLLAMA_TOKEN
        self.model = "deepseek-v3.1:671b"
        self.user_role = "user"
        self.assistant_role = "assistant"
        self.response = ""
        self.messages_history = []

        self.initChat()
        # self.initMessage()
        # self.saveResponse()

    def initChat(self):
        self.client = Client(
            host=self.host,
            headers={"Authorization": self.token}
        )

    def initMessage(self):
        message = {
            "role": self.user_role,
            "content": """You are my personal AI assistant. 
            Your main purpose to help me with my tasks that I will sent to you.
            You must to follow and remember next rules:

            1. DON'T USE IT:
            **bold text** or *italics*
            Headings with ## or ===
            Citation blocks with >
            Unnecessary delimiters --- or ***
            Emojis and decorations
            
            2. USE IT ONLY FOR THE CODE:
            ```language ... ``` for code blocks
            `inline_code` for individual elements
            Regular comments // or # in the code 
            
            3. Respond with clear text without Markdown markup.
            4. Use the usual line breaks and indents.
            """
        }
        self.messages_history.append(message)
        self.response = self.client.chat(self.model, messages=self.messages_history)

    def sendMessage(self, content):
        message = {
            "role": self.user_role,
            "content": content
        }
        self.messages_history.append(message)
        self.response = self.client.chat(self.model, messages=self.messages_history)
    
    def saveResponse(self):
        self.messages_history.append({
            "role": self.assistant_role,
            "content": self.response.message.content
        })

    def getResponse(self):
        self.saveResponse()
        return self.response.message.content

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