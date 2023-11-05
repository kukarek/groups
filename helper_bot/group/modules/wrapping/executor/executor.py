import requests
import time
import random
import threading
from logging import Logger
from misc.config import API_URL, API_KEY




class Executor:


    logg: Logger = None
    isActiveWrapping = False
    GROUP_NAME = None

    def get_balance(self):

        params = dict(key=API_KEY, action="balance")
        
        res = requests.get(API_URL, params=params)

        if res.status_code != 200:
            self.logg.error(f"Не удалось получить баланс: status code - {res.status_code}")
            return "ошибка :("
        balance = float(res.json()['balance'])
        return round(balance, 2)

    def __get_vk_posts_id(self, url):  #принимает url страницу группы 
        
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

    def start_wrapp(self):

        if self.isActiveWrapping == False:

            self.isActiveWrapping = True

            t1 = threading.Thread(target=self.wrapp)
            t1.start()

    def __sleep(self, minutes): #пауза с проверкой 

        for _ in range(0, minutes * 60):

            time.sleep(1) 

            if not self.isActiveWrapping:
                return None
            
        return "Ok"

    def wrapp(self): 

        while True:

            posts_id = self.__get_vk_posts_id(f"https://vk.com/{self.GROUP_NAME}")
        
            quantity = random.randint(100, 110)
            
            for j in range(0, 8):

                params = dict(key=API_KEY, action="add", service=879, link=f"https://vk.com/wall-{posts_id[j]}", quantity=quantity)
                res = requests.get(API_URL, params=params)
                order_status = res.json()
                print(f"group({self.GROUP_NAME}) {order_status}")

                if "error" in order_status:
                    self.logg.error(f"Не удалось создать ордер накрутки для ВК: {order_status['error']}")
                

            if self.__sleep(30) != "Ok":
                self.isActiveWrapping = False
                return   # 30 минут пауза с проверкой
        
        
      

