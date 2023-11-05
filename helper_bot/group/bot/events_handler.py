from helper_bot.group.bot.handlers.message_handlers.message_handler import MessageHandler
from helper_bot.group.bot.handlers.wallpost_handlers.wallpost_handler import WallPostHandler

class EventHandler(MessageHandler, WallPostHandler):

    async def message_handler(self, vk, event, vk_session):

        try:
            response = self.reply_message_handler(event=event, vk_session=vk_session)

            await self.send_answer(response=response, vk=vk, event=event, vk_session=vk_session)
            await self.notife_admin(response=response, vk=vk, event=event)
        except Exception as e:
            self.logg.error(e)

    async def wallpost_handler(self, vk, event):

        try:
            #рассылка поста подписчикам
            await self.sending_post_to_users(vk, event)
        except Exception as e:
            self.logg.error(e)
    