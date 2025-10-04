from ollama import Client


class Ollama_chat():
    def __init__(self):
        self.host = "https://ollama.com"
        self.token = 'a64be015a40246dc983de3e4b0fe852e.fUE1BNcoRPbRNmGFHIygICpe'
        self.model = 'gpt-oss:120b'
        self.role = 'user'
        self.response = ''

        self.initChat()
        # self.initMassage()

    def initChat(self):
        self.client = Client(
            host=self.host,
            headers={'Authorization': self.token}
        )

    # def initMassage(self):
    #     messages = [
    #       {
    #         'role': self.role,
    #         'content': """You are my personal AI assistant. 
    #         Your main purpose to help me with my tasks that I will sent to you.
    #         You must to follow and remember next rules:

    #         1. DON'T USE IT:
    #         **bold text** or *italics*
    #         Headings with ## or ===
    #         Citation blocks with >
    #         Unnecessary delimiters --- or ***
    #         Emojis and decorations
            
    #         2. USE IT ONLY FOR THE CODE:
    #         ```language ... ``` for code blocks
    #         `inline_code` for individual elements
    #         Regular comments // or # in the code 
            
    #         3. Respond with clear text without Markdown markup.
    #         4. Use the usual line breaks and indents.
    #         """,
    #       },
    #     ]
    #     for part in self.client.chat(self.model, messages=messages, stream=True):
    #         self.response.append(part['message']['content'])

    def sendMassage(self, message):
        messages = [
            {
                'role': self.role,
                'content': """You are my personal AI assistant. 
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
                """,
            },
            {
                'role': self.role,
                'content': message,
            },
        ]
        self.response = self.client.chat(self.model, messages=messages)

    def getResponse(self):
        response = self.response
        self.clearResponse()
        return response
    
    def getClient(self):
        return self.client
    
    def clearResponse(self):
        self.response = ''
    