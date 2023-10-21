from aiogram.types import Message
from ..functions import vk_top
from ..functions import wrapping
from misc.config import GROUPCHLB_ID, GROUPCHLB_LINK, GROUPKZN_ID, GROUPKZN_LINK
from aiogram.types import Message

async def on_start(message: Message):

    await message.answer("Привет! Я бот. Напиши мне что-нибудь!")

async def get_top(message: Message):
   
    topchlb = vk_top.Get_top(url = GROUPCHLB_LINK, group_id = GROUPCHLB_ID)
    topkzn = vk_top.Get_top(url = GROUPKZN_LINK, group_id = GROUPKZN_ID)

    await message.answer(f"Место в топе по Челябинску: {topchlb}\n"
                         f"Место в топе по Казани: {topkzn}")
    
async def on_help(message: Message):

    await message.answer("Я - простой бот, который отвечает на команды. "
                         "Доступные команды:\n"
                         "/start - Начать общение с ботом\n"
                         "/help - Получить справку\n"
                         "/get_top - получить номер в поиске\n"
                         "stop_wrapping\n"
                         "start_wrapping\n"
                         "cycle=0..27\n"
                         "VK=bool\n"
                         "TG=bool\n"
                         "status - состояние накрутки\n"
                         "выражения пишуться через 1 пробел\n"
                         "/balance - текущий баланс счета")
                             
async def balance(message: Message):
    
    balance = wrapping.get_balance()
    await message.answer(f"Текущий баланс: {balance}")

async def status(message: Message):
    
    await message.answer(wrapping.status())
    
async def echo(message: Message):
    """
    принимает команду накрутки по ключевым словам 
    может устанавливать отдельные состояния накрутки

    """
    cycle = 0
    VK = True
    TG = True
    timer = 0

    text = message.text
    
    try:
     if text.find("stop_wrapping") != -1:
        wrapping.wrapping_state.isActive = False
        await message.answer("Остановка накрутки")

     elif text.find("start_wrapping") != -1:
        
        if text.find("cycle") != -1:
            ss =  text.split('cycle=')[1]
            sss = ss.split(' ')[0]
            cycle = int(sss)
        
        if text.find("VK") != -1:
            ss =  text.split('VK=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               VK = False    

        if text.find("TG") != -1:
            ss =  text.split('TG=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               TG = False

        if text.find("timer") != -1:
            ss =  text.split('timer=')[1]
            sss = ss.split(' ')[0]
            timer = int(sss)

        if wrapping.start_wrapping(cycle=cycle,VK=VK,TG=TG, timer=timer):
           await message.answer(f"Запуск накрутки: cycle={cycle}, VK={VK}, TG={TG}, timer={timer}")
        else:
           await message.answer("Накрутка уже запущена, либо поток еще не завершил свой крайний цикл")

     elif text.find("VK") != -1 or text.find("TG") != -1: #меняет статус накрутки тг и вк
        
        if text.find("VK") != -1:
            ss =  text.split('VK=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               VK = False   
            await message.answer(f"Установка параметров: VK={VK}")

        if text.find("TG") != -1:
            ss =  text.split('TG=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               TG = False
            await message.answer(f"Установка параметров: TG={TG}")

        wrapping.wrapping_state.VK = VK
        wrapping.wrapping_state.TG = TG

     else:
        await message.answer(f"Вы написали: {message.text}")

    except Exception as e: 
        await message.answer(e)

