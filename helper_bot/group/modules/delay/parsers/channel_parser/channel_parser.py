from bs4 import BeautifulSoup
import requests
from logging import Logger
from .post import Post
import random
import datetime

class Channel_Parser():

    def __init__(self, channel: str, logg, default_photo = None) -> None:
        self.key = "Channel_Parser"
        self.resource = self.create_link(channel)
        self.logg = logg
        self.default_photo = default_photo

    def create_link(self, channel):

        return channel.replace("https://t.me/", "https://t.me/s/")

    def get_actually_day(self, day) -> int:

        current_date = datetime.datetime.now()
        now_day = current_date.day

        if day == "Завтра":
            return str(now_day)
        else:
            return str(now_day - 1)

    def get_actually_posts(self, posts, actually_day) -> []:
        # оставляем только посты с нужной датой
        actually_posts = []

        for post in posts:

            # Находим элемент <time> с классом 'time'
            time_element = post.find('time', class_='time')

            # Получаем значение атрибута 'datetime'
            datetime_value = time_element['datetime']

            # Разбираем значение атрибута 'datetime' и извлекаем число "28"
            date_parts = datetime_value.split('T')[0].split('-')
            day = date_parts[2]

            if day[0] == '0':
                day = day[1]

            if day == actually_day:

                actually_posts.append(post)
            
        return actually_posts

    def parse(self, day, posts):
        
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        response = requests.get(self.resource, headers=headers)

        if response.status_code == 200:
            # Парсим HTML-код страницы

            soup = BeautifulSoup(response.text, 'html.parser')

            posts_html = soup.find_all('div', class_='tgme_widget_message_wrap')
           
            actually_day = self.get_actually_day(day)

            actually_posts_html = self.get_actually_posts(posts_html, actually_day)

            for soup in actually_posts_html:

                post = Post()
                post.set_id(random.randint(0, 100000))

                # Ищем все элементы <br> и добавляем после них новую строку
                br_elements = soup.find_all('br')
                for br in br_elements:
                    br.insert_after("\n")

                # Ищем все элементы <i> с классом "emoji" и извлекаем их содержимое
                emoji_elements = soup.find_all('i', class_='emoji')
                for emoji in emoji_elements:
                    emoji_text = emoji.b.get_text()  # Извлекаем смайлик из элемента <b>
                    emoji.replace_with(emoji_text)  # Заменяем элемент <i> на смайлик

                # Извлекаем текст из элемента <div>
                div_element = soup.find('div', class_='tgme_widget_message_text')
                parsed_text = div_element.get_text()
                    
                post.set_text(parsed_text)

                if self.default_photo:
                    post.set_image(self.default_photo)

                posts.append(post)
            

        else:
            self.logg.error(f"Не удалось выполнить запрос к {self.resource}, код {response.status_code} ")
    
    """
    def load_image(self, link):

        #загрузка фото 
        response = requests.get(link)

        if response.status_code == 200:
            
            #получение данных из ответа
            image_data = io.BytesIO(response.content)

            # Инициализация сессии ВКонтакте
            session = vk_api.VkApi(token=GROUPKZN_ID)
            vk = session.get_api()

            # Загрузка фотографии в альбом группы
            upload = vk_api.VkUpload(vk)
            photo = upload.photo(photos=image_data, group_id=GROUPKZN_ID, album_id=234078005)

            # Получение информации о загруженной фотографии
            photo_info = photo[0]

        
        return photo_info
    """

