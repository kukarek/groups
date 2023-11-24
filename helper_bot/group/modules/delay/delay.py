from .parsers import Channel_Parser
import vk_api
from datetime import datetime, timedelta, date
import random
from .parsers.channel_parser import Channel_Parser
from .parsers.group_parser import Group_Parser
import requests

class Delay():

    logg = None

    DEFAULT_POST_PHOTO = None

    VK_TOKEN_FOR_DELAY = None

    posts = []

    GROUP_ID = None

    parsers = [

    ]

    day = "Завтра"
    start_hour = 8
    end_hour = 22

    def set_default_photo(self, photo):
        
        response = requests.get(url=f"https://vk.com/{photo}")

        if response.status_code == 200:
            self.DEFAULT_POST_PHOTO = photo

            for parser in self.parsers:
                if parser.key == "Channel_Parser":

                    parser.default_photo = photo
                    
            return True
        else:  
            return False

    def get_parsers(self) -> []:
        return self.parsers
    
    def add_channel_parser(self, channel_link):

        parser = Channel_Parser(channel_link, self.logg, self.DEFAULT_POST_PHOTO)
        self.parsers.append(parser)

    def add_group_parser(self, channel_link):

        parser = Group_Parser(channel_link, self.logg, self.DEFAULT_POST_PHOTO)
        self.parsers.append(parser)
    
    def remove_parser(self, parser_link):

        for p in self.parsers:
            if p.resource == parser_link:
                self.parsers.remove(p)

    def get_posts(self) -> []:

        for parser in self.parsers:
            parser.parse(self.day, self.posts)

        random.shuffle(self.posts)
        return self.posts
    
    def remove_post(self, post_id: int):

        for post in self.posts:
            if post.id == post_id:
                self.posts.remove(post)

    def remove_all_post(self):

        self.posts.clear()

    def make_def(self) -> bool:

        vk_session = vk_api.VkApi(token=self.VK_TOKEN_FOR_DELAY)
        vk = vk_session.get_api()

        try: 
            for post in self.posts:
            
                while True:
                
                    #если на это время уже стоит пост, пробуем другое время
                    self.set_random_time(post)
                    if self.make_post_in_def(vk, post):
                        break 
            return True
        
        except Exception as e:
            self.logg.error(e)
            return False   

    def make_post_in_def(self, vk, post) -> bool:

        try:
            vk.wall.post(owner_id=f"-{self.GROUP_ID}", message=post.text, publish_date=post.datetime, attachments=post.image)  
            return True
        
        except Exception as e:
            
            if e.code == 214:
                return False
            else:
                raise e

    def tomorrow_date(self) -> str:

        tom = date.today() + timedelta(days=1)

        datetime_obj = datetime(tom.year, tom.month, tom.day)

        unix_timestamp = int(datetime_obj.timestamp())

        return unix_timestamp
    
    def now_date(self) -> str:

        now = datetime.now()

        datetime_obj = datetime(now.year, now.month, now.day)

        unix_timestamp = int(datetime_obj.timestamp())

        return unix_timestamp

    def set_random_time(self, post):

        hour = random.randint(self.start_hour, self.end_hour) * 60 * 60
        minute = random.randint(0, 59) * 60
        unix_timestamp = self.get_unix_timestamp() + hour + minute

        post.set_time(unix_timestamp)

    def get_unix_timestamp(self):

        choose_date_list = {
        "Сегодня": self.now_date,
        "Завтра": self.tomorrow_date
        }

        return choose_date_list[self.day]()

    def set_date(self, day):
        self.day = day

    def set_start_hour(self, hour):

        try:
            hour = int(hour)
            if self.day == "Сегодня":

                now = datetime.now()
                if now.hour >= hour:
                    raise Exception()

            if self.end_hour <= hour:
                raise Exception()
            
            if hour > 22:
                raise Exception()
            
            self.start_hour = hour
            return True
        except:
            return False

    def set_end_hour(self, hour):

        try:
            hour = int(hour)
            if self.day == "Сегодня":

                now = datetime.now()
                if now.hour >= hour:
                    Exception()

            if self.start_hour >= hour:
                Exception()

            if hour > 23:
                raise Exception()

            self.end_hour = hour
            return True
        except:
            return False
        
    def set_vk(self, vk):
        self.vk = vk
    

        