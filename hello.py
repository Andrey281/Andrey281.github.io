import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import re
import requests
import random

token = "81c628d00dc4c6a029831da4fc17fa05ea9336cf03fa2daadb6d23c122eac6e24f9df8a7e620a45f4918f"
vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

kid = {}
ktok = {}
mess = {}
kolvo = {}
balance = {}
stavka = {}


def encodeUrl(str1):
    str1 = str1.replace(' ', r'+')
    str1 = str1.replace('\n', r'0A')
    return str(str1)

def create_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)

    keyboard.add_button("Привит", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
    keyboard.add_button("Начать", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)

    return keyboard.get_keyboard()

def write_msg(user_id, message):
    keyboard = create_keyboard()
    vk.method('messages.send', {'user_id': user_id, 'message': message,'keyboard':  keyboard, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print('qq')
            request = event.text
            keyboard = create_keyboard()
            
            if re.search(r'азино \d+',request):
                stavka[event.user_id] = request.split()[1]
                if len(balance) == 0 or balance[event.user_id] == None:
                    balance[event.user_id] = 1000000
                if int(stavka[event.user_id]) <= int(balance[event.user_id]):
                    k = random.randint(1,4)
                    if k == 1:
                        balance[event.user_id] = int(balance[event.user_id]) + int(stavka[event.user_id])
                        write_msg(event.user_id, "Поздравляю, вы выйграли "+stavka[event.user_id]+" (х2)&#129297;\n &#128181;Ваш баланс: "+str(balance[event.user_id]))
                    elif k == 2:
                        balance[event.user_id] = int(balance[event.user_id]) - int( float(stavka[event.user_id]) * 0.25 ) 
                        write_msg(event.user_id, "К сожалению, вы проиграли "+str(float(stavka[event.user_id]) * 0.25 )+" (0.75х)&#128532;\n &#128181;Ваш баланс: "+str(balance[event.user_id]))
                    elif k == 3:
                        balance[event.user_id] = int(balance[event.user_id]) - int( float(stavka[event.user_id]) * 0.5 ) 
                        write_msg(event.user_id, "К сожалению, вы проиграли "+str(float(stavka[event.user_id]) * 0.5 )+" (0.5х)&#128532;\n &#128181;Ваш баланс: "+str(balance[event.user_id]))
                    elif k == 4:
                        balance[event.user_id] = int(balance[event.user_id]) - int( float(stavka[event.user_id]) * 0.75 ) 
                        write_msg(event.user_id, "К сожалению, вы проиграли "+str(float(stavka[event.user_id]) * 0.75 )+" (0.25х)&#128532;\n &#128181;Ваш баланс: "+str(balance[event.user_id]))
                else:
                    write_msg(event.user_id, "Вы хотели поставить "+stavka[event.user_id]+", но не смогли это сделать, т.к не хватает средств на балансе.")


            if request == "Привит":
                write_msg(event.user_id, "Хай")
            elif request == "Начать":
                write_msg(event.user_id, "Для отправки укажите токен, с которого отправлять! tok [токен]")
            elif re.search(r"id \d+", request):
                kid[event.user_id] = request.split()[1]
                write_msg(event.user_id,'ID отправки: ' + str(kid[event.user_id]) + '. Теперь напишите сообщение, которое отправить. mes: [сообщение]')
            elif re.search(r"tok .+", request):
                ktok[event.user_id] = request.split()[1]
                write_msg(event.user_id,'Токен отправки: '+ktok[event.user_id]+'. Отправьте Айди, которому отправить. id [id]')
            elif re.search(r"mes: .+", request):
                mess[event.user_id] = request.split(': ')[1]
                write_msg(event.user_id,"Окей, для отправки напишите 'Отправить' ! Ваше сообщение по стандарту отправлено 1 раз. Чтобы изменить число отправок - 'Кол [кол-во]'")
            elif re.search(r'кол \d+', request):
                kolvo[event.user_id] = request.split()[1]
                write_msg(event.user_id,"Вы изменили кол-во отправленных сообщений на "+kolvo[event.user_id])
            elif request == 'Отправить':
                #print(mess[event.user_id]+ktok[event.user_id]+kid[event.user_id])
                if len(mess) == 0 or len(ktok) == 0 or len(kid) == 0 or ktok[event.user_id] == None or kid[event.user_id] == None or mess[event.user_id] == None:
                    write_msg(event.user_id,"Проверьте, все ли аргументы вы указали !")
                else:
                    if len(kolvo) == 0 or kolvo[event.user_id] == None:
                        requests.get('https://api.vk.com/method/messages.send?v=5.103&message='+encodeUrl(mess[event.user_id])+'&user_id='+str(kid[event.user_id])+'&access_token='+ktok[event.user_id]+'&random_id=0')
                        write_msg(event.user_id,"Ваше сообщение доставлено адрессату ")
                    else:
                        for i in range(int(kolvo[event.user_id])):
                            response = requests.get('https://api.vk.com/method/messages.send?v=5.103&message='+encodeUrl(mess[event.user_id])+'&user_id='+str(kid[event.user_id])+'&access_token='+ktok[event.user_id]+'&random_id=0')
                        write_msg(event.user_id,"Ваше сообщение доставлено адрессату "+kolvo[event.user_id]+' раз')
                       
            
            #write_msg(event.user_id,ktok + '    ' + str(kid) + '  ' + str(mess))


