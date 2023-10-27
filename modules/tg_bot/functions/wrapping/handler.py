import requests
import time
import random
import threading
import logging
from . import states
from misc.config import API_URL, API_KEY, kzn_url, tg_kzn_url

logg = logging.getLogger(__name__)

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

def start_wrapping():

    states.wrapping.start()

    t1 = threading.Thread(target=wrapp)
    t1.start()

def sleep(seconds): #пауза с проверкой 

    states.wrapping.timer = seconds
    
    seconds *= 60

    for a in range(0, seconds):

        if states.wrapping.timer != 0 and a > 0 and a % 60 == 0:
            states.wrapping.timer -= 1

        time.sleep(1) 
        if not states.wrapping.isActive:
            states.wrapping.stop()
            return None
        
    states.wrapping.timer = 0
    return "Ok"

def wrapp(): 

    for states.wrapping.cycle in range(states.wrapping.cycle, 28):    #цикл на 14 часов, каждые 30 минут 
        
        if sleep(states.wrapping.timer) != "Ok":
            return
          
        kzn_posts_id = get_vk_posts_id(kzn_url)
        tg_kzn_posts_id = get_tg_posts_id(tg_kzn_url)
    
        e = 5 if states.wrapping.cycle < 20 else 10

        for j in range(e):  
            quantity = random.randint(100, 110)

            if states.wrapping.VK:
            
                params = dict(key=API_KEY, action="add", service=879, link=f"https://vk.com/wall-{kzn_posts_id[j]}", quantity=quantity)
                res = requests.get(API_URL, params=params)
                order_status = res.json()
                print(f"vk kzn {order_status}")

                if "error" in order_status:
                    logg.error(f"Не удалось создать ордер накрутки для ВК: {order_status['error']}")
                                    
            if states.wrapping.TG:
            
                params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[j]}", quantity=100)
                res = requests.get(API_URL, params=params)
                order_status = res.json()
                print(f"tg kzn {order_status}")

                if "error" in order_status:
                    logg.error(f"Не удалось создать ордер накрутки для TG: {order_status['error']}")

        print(f"цикл: {states.wrapping.cycle}") 

        if sleep(30) != "Ok":
            return   # 30 минут пауза с проверкой
        
    states.wrapping.stop()
      
      

