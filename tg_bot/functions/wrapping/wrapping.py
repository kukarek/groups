import requests
import time
import random
import threading
from .states import States
from misc.config import API_URL, API_KEY, kzn_url, tg_kzn_url


wrapping_state = States()

def get_balance():

    params = dict(key=API_KEY, action="balance")
    res = requests.get(API_URL, params=params)
    return res.json()['balance']

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

    for a in range(0, seconds):

        if wrapping_state.timer != 0:
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

    for wrapping_state.cycle in range(28):    #цикл на 14 часов, каждые 30 минут 
          
        kzn_posts_id = get_vk_posts_id(kzn_url)
        tg_kzn_posts_id = get_tg_posts_id(tg_kzn_url)
    
        if wrapping_state.cycle < 20:
    
            for j in range(5):  #накрут последних четырех + закреп в течение 10 часов 
                quantity = random.randint(100, 110)

                if wrapping_state.VK:
                
                    params = dict(key=API_KEY, action="add", service=879, link=f"https://vk.com/wall-{kzn_posts_id[j]}", quantity=quantity)
                    res = requests.get(API_URL, params=params)
                    print(f"kzn {str(res.json())}")
                
                if wrapping_state.TG:
                
                    params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[j]}", quantity=100)
                    res = requests.get(API_URL, params=params)
                    print(f"tg kzn {str(res.json())}")

            print("накрутка последних четырех!")


        if wrapping_state.cycle > 19:

            for k in range(10):  #накрут последних девяти в течение 4 часов
                quantity = random.randint(90, 110)
    
                if wrapping_state.VK: 

                    params = dict(key=API_KEY, action="add", service=879, link=f"https://vk.com/wall-{kzn_posts_id[k]}", quantity=quantity)
                    res = requests.get(API_URL, params=params)
                    print(f"kzn {str(res.json())}")
    
                if wrapping_state.TG:
        
                    params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[k]}", quantity=100)
                    res = requests.get(API_URL, params=params)
                    print(f"tg kzn {str(res.json())}")
                    
            print("накрутка последних десяти!")
    

        print(f"цикл: {wrapping_state.cycle}") 

        if sleep(1800) != "Ok":
            return   # 30 минут пауза с проверкой
    
      
      

