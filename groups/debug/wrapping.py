"""
Работает как библиотека
   
"""
import schedule
import requests
import time
import random
import threading
from config import API_URL, API_KEY, kzn_url, tg_kzn_url

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

class States: #содежит состояния накрутки
    
    stop = True  #остановка накрутки после завершения текущего цикла, если значение True
    VK = True #если значение False, вк не крутиться
    TG = True #если значение False, тг не крутиться
    cycle = 0
    message = None

active_threads = [] #отслеживание активных потоков

def status():
          
    if States.message != None:
        return States.message
    elif States.stop == False:
        return f"VK = {States.VK}, TG = {States.TG}, cycle = {States.cycle}"
    else:
        return f"автонакрутка неактивна"

def start_wrapping(cycle = 0, VK = True, TG = True, timer = 0):
 
    if not active_threads:
        t1 = threading.Thread(target=wrapping, args=(cycle, VK, TG, timer))
        t1.start()
        active_threads.append(t1)
        return True  #поток запущен
    else:
        return False  #поток не запущен
    
def sleep(seconds): #пауза с проверкой 
    a = 0
    while a < seconds:
        time.sleep(1) 
        if States.stop:
            active_threads.clear()
            return None
        a += 1
    return "Ok"
    

def wrapping(cycle, VK, TG, timer): 
  
    States.VK = VK
    States.TG = TG
    States.stop = False
    i = cycle
    
    if sleep(timer*60) != "Ok":
        return

    try:
        while i < 28:    #цикл на 14 часов, каждые 30 минут 
            if States.stop == False:    
                kzn_posts_id = get_vk_posts_id(kzn_url)
                tg_kzn_posts_id = get_tg_posts_id(tg_kzn_url)
            
                if i < 20:
            
                    j = 0
                    while j < 5:  #накрут последних четырех + закреп в течение 10 часов 
                        quantity = random.randint(90, 110)

                        if States.VK:
                        
                            params = dict(key=API_KEY, action="add", service=879, link=f"https://vk.com/wall-{kzn_posts_id[j]}", quantity=quantity)
                            res = requests.get(API_URL, params=params)
                            print(f"kzn {str(res.json())}")
                        
                        if States.TG:
                        
                            params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[j]}", quantity=100)
                            res = requests.get(API_URL, params=params)
                            print(f"tg kzn {str(res.json())}")

                        if j == 4:
                            print("накрутка последних четырех!")

                        j += 1

                if i > 19:
        
                    k = 0
                    while k < 10:  #накрут последних девяти в течение 4 часов
                        quantity = random.randint(90, 110)
            
                        if States.VK: 

                            params = dict(key=API_KEY, action="add", service=879, link=f"https://vk.com/wall-{kzn_posts_id[k]}", quantity=quantity)
                            res = requests.get(API_URL, params=params)
                            print(f"kzn {str(res.json())}")
            
                        if States.TG:
                
                            params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[k]}", quantity=100)
                            res = requests.get(API_URL, params=params)
                            print(f"tg kzn {str(res.json())}")
                            
                        if k == 9:
                            print("накрутка последних десяти!")
            
                        k += 1

                print(f"цикл: {i}") 

                States.cycle = i  

                if i == 27:
                    States.stop = True
                    active_threads.clear() #перед завершением функции чистим список активных потоков

                if sleep(1800) != "Ok":
                    return   # 30 минут пауза с проверкой

                i += 1 
            else:
                active_threads.clear() #перед завершением функции чистим список активных потоков
                break
    
    except Exception as e:
        active_threads.clear()
        States.message = e
      
      

