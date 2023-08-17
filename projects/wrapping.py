import requests
import time
import random
import threading

API_KEY = "bb8cad79840056d1fff7676360a48b97"
API_URL = "https://prosmmtop.ru/api/v2"
kzn_url = "https://vk.com/rabotakazank"
chlb_url = "https://vk.com/rabotachelyabynsk"
tg_kzn_url = "https://t.me/s/rabotakazank"
tg_chlb_url = "https://t.me/s/rabotachelyabinski"
"""
def start_vk_wrapping(post_id):

    return resp


def start_tg_wrapping(post_id):

    return resp

"""


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

    if url == tg_chlb_url:
        arc = html.split('data-post="rabotachelyabinski/')
        for post in arc:
          post_id = post.split('"')[0]
          posts_id.append(post_id)

    posts_id.reverse()

    return posts_id  #возвращает список id последних девяти постов

stop = False

def main():  #заменяем имя функции и используем для внешних вызовов

  start_wrapping()

  
def start_wrapping():
  t1 = threading.Thread(target=wrapping)
  t1.start()
  print("Накрутка запущена в отдельном потоке!")
  t1.join()

def wrapping(): 
  

  i = 18
  while i < 28:    #цикл на 14 часов, каждые 30 минут 
   if stop == False:    
     kzn_posts_id = get_vk_posts_id(kzn_url)
     chlb_posts_id = get_vk_posts_id(chlb_url)
     tg_kzn_posts_id = get_tg_posts_id(tg_kzn_url)
     tg_chlb_posts_id = get_tg_posts_id(tg_chlb_url)
    
     if i < 20:
       
       j = 0
       while j < 5:  #накрут последних четырех + закреп в течение 10 часов 
          quantity = random.randint(90, 110)
          """
          params = dict(key=API_KEY, action="add", service=838, link=f"https://vk.com/wall-{kzn_posts_id[j]}", quantity=quantity)
          res = requests.get(API_URL, params=params)
          print(f"kzn {str(res.json())}")

          params = dict(key=API_KEY, action="add", service=838, link=f"https://vk.com/wall-{chlb_posts_id[j]}", quantity=quantity)
          res = requests.get(API_URL, params=params)
          print(f"chlb {str(res.json())}")
          """
          params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[j]}", quantity=100)
          res = requests.get(API_URL, params=params)
          print(f"tg kzn {str(res.json())}")

          params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotachelyabinski/{tg_chlb_posts_id[j]}", quantity=100)
          res = requests.get(API_URL, params=params)
          print(f"tg chlb {str(res.json())}")
          
          if j == 4:
           print("накрутка последних четырех!")

          j += 1

     if i > 19:
       
       k = 0
       while k < 10:  #накрут последних девяти в течение 4 часов
          quantity = random.randint(90, 110)
          
          params = dict(key=API_KEY, action="add", service=838, link=f"https://vk.com/wall-{kzn_posts_id[k]}", quantity=quantity)
          res = requests.get(API_URL, params=params)
          print(f"kzn {str(res.json())}")

          params = dict(key=API_KEY, action="add", service=838, link=f"https://vk.com/wall-{chlb_posts_id[k]}", quantity=quantity)
          res = requests.get(API_URL, params=params)
          print(f"chlb {str(res.json())}")
          """
          params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotakazank/{tg_kzn_posts_id[k]}", quantity=100)
          res = requests.get(API_URL, params=params)
          print(f"tg kzn {str(res.json())}")

          params = dict(key=API_KEY, action="add", service=614, link=f"https://t.me/rabotachelyabinski/{tg_chlb_posts_id[k]}", quantity=100)
          res = requests.get(API_URL, params=params)
          print(f"tg chlb {str(res.json())}")
          """
          if k == 9:
           print("накрутка последних десяти!")
          
          k += 1

     print(f"цикл: {i}")   
     time.sleep(1800)     # 30 минут пауза
     i += 1 
   else:
      break 


      

 


  
if __name__ == '__main__':
  main()
