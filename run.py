import threading
import vk_bot.bot.main
import tg_bot.bot.main

if __name__=="__main__":
   
    threadings = [threading.Thread(target=vk_bot.bot.main.start_bot)]


    for thread in threadings:
        thread.start()
    
    tg_bot.bot.main.start_bot()

    for thread in threadings:
        thread.join()

