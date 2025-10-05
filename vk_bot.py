import vk_api
import config
from ollama_logic import Ollama_chat
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})

# API-ключ созданный ранее
token = config.VK_TOKEN

data = []

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

chat = Ollama_chat()

# Основной цикл
try:
    
    for event in longpoll.listen():

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:
        
            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:
            
                # Сообщение от пользователя
                request = event.text

                chat.sendMessage(request)
                response = chat.getResponse()
                user_id = event.user_id
                write_msg(user_id, response)

                # data.append({"user_id": user_id, "messages_history":chat.})

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Saving up...")



    # Perform any necessary cleanup actions here
    print("Save complete. Exiting program.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    print("VK bot end")


# def saveState():
    