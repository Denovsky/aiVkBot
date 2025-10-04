import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})

# API-ключ созданный ранее
token = "vk1.a.YLGlifHC7g2PyM2gSf0GfpXtG8YJIK0uGj94sv1Jl1JoZZBFQJrzXV9Q2VkXAnE6fTSsyZ3e9QozeHuTlJpqmL0PEGdvgGceE_ZCuU4RdL62kxS7cUh0tGtXmWtbLDxqTcTTeapM05ikGC8R40Fctvx1uoEOGWe_kBVNyTqOzpX84si77SX1SwwH8Dv3QKS0nL4n9e4p3jOX_gPg0HLeyA"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
    
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
        
            # Сообщение от пользователя
            request = event.text
            
            # Каменная логика ответа
            if request == "привет":
                write_msg(event.user_id, "Хай")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")