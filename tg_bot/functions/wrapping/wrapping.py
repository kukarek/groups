import requests
import time
import random
import threading
import logging
from .states import States
from log import ERROR
from misc.config import API_URL, API_KEY, kzn_url, tg_kzn_url

logg = logging.getLogger(__name__)
logg.addHandler(ERROR())

wrapping_state = States()

def get_balance():
    
    params = dict(key=API_KEY, action="balance")
    
    res = requests.get(API_URL, params=params)

    if res.status_code != 200:
        logg.error(f"Не удалось получить баланс: status code - {res.status_code}")
        return "ошибка :("
    balance = float(res.json()['balance'])
    return round(balance, 2)

def get_vk_posts_id(url):  #принимает url страницу группы 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    html = response.text

    posts_id = []
    
    arc = html.split('div id="post-')
    arc.pop(0)
    #arc.pop(0)
    for post in arc:
        post_id = post.split('"')[0]
        posts_id.append(post_id)

    return posts_id  #возвращает список id последних девяти постов

def get_tg_posts_id(url):  #принимает url страницу группы 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    html = response.text

    posts_id = []
    if url == tg_kzn_url:
        arc = html.split('data-post="rabotakazank/')
        for post in arc:
            post_id = post.split('"')[0]
            posts_id.append(post_id)

    posts_id.reverse()

    return posts_id  #возвращает список id последних девяти постов

def status():
          
    if wrapping_state.isActive:
        return f"VK = {wrapping_state.VK}, TG = {wrapping_state.TG}, cycle = {wrapping_state.cycle}, timer = {wrapping_state.timer}"
    else:
        return f"автонакрутка неактивна"

def start_wrapping(cycle = 0, VK = True, TG = True, timer = 0):
 
    global wrapping_state

    if not wrapping_state.isActive:

        wrapping_state.start(cycle = cycle, VK = VK, TG = TG, timer = timer)

        t1 = threading.Thread(target=wrapping)
        t1.start()
        return True  #поток запущен
    else:
        return False  #поток не запущен

def on_stop_wrapping():
    
    wrapping_state.stop()

def sleep(seconds): #пауза с проверкой 

    wrapping_state.timer = seconds
    
    seconds *= 60

    for a in range(0, seconds):

        if wrapping_state.timer != 0 and a > 0 and a % 60 == 0:
            wrapping_state.timer -= 1

        time.sleep(1) 
        if not wrapping_state.isActive:
            on_stop_wrapping()
            return None
        
    wrapping_state.timer = 0
    return "Ok"

def wrapping(): 

    global wrapping_state

    if sleep(wrapping_state.timer) != "Ok":
        return

    for wrapping_state.cycle in range(wrapping_state.cycle, 28):    #цикл на 14 часов, каждые 30 минут 
          
        kzn_posts_id = get_vk_posts_id(kzn_url)
        tg_kzn_posts_id = get_tg_posts_id(tg_kzn_url)
    
        e = 5 if wrapping_state.cycle < 20 else 10

        for j in range(e):  
            quantity = random.randint(100, 110)

            if wrapping_state.VK:
            
                params = dict(key=API_KEY, action="add", service=879, link=f"https://vk.com/wall-{kzn_posts_id[j]}", quantity=quantity)
                res = requests.get(API_URL, params=params)
                order_status = res.json()
                print(f"vk kzn {order_status}")

                if "error" in order_status:
                    logg.error(f"Не удалось создать ордер накрутки для ВК: {order_status['error']}")
                                    
            if wrapping_state.TG:
            
                params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[j]}", quantity=100)
                res = requests.get(API_URL, params=params)
                order_status = res.json()
                print(f"tg kzn {order_status}")

                if "error" in order_status:
                    logg.error(f"Не удалось создать ордер накрутки для TG: {order_status['error']}")

        print(f"цикл: {wrapping_state.cycle}") 

        if sleep(30) != "Ok":
            return   # 30 минут пауза с проверкой
    
      
      

