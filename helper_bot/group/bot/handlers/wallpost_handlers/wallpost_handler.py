import logging
from database import sql
from logging import Logger

class WallPostHandler:

    logg: Logger = None

    async def sending_post_to_users(self, vk, event):
        
        post = event.object

        users = sql.get_users_data_as_dict(group_id=abs(post.owner_id))
        
        matching_users = []

        self.logg.debug("finding users with matching keywords")
        for user in users:
            
            user_id = user['user_id']
            keywords = user['keywords']

            keyword_list = keywords.split(',')

            for keyword in keyword_list:
                if keyword in post.text.lower():
                    matching_users.append(user_id)
                    break  # Для оптимизации - если слово найдено, выходим из внутреннего цикла
        
        if matching_users:
            self.logg.debug(f"sending wallpost to users ({len(matching_users)}) with matching keywords")
            for user in users: #рассылаем пост
                self.logg.debug(f"sending wallpost to user {user}")
                vk.messages.send(user_id=user["user_id"], message="Новый пост!", attachment=f"wall-22156807_{event.object.id}", random_id=0)

