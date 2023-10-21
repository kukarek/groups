import threading
import vk_bot.bot.main
import tg_bot.bot.main
import log

if __name__=="__main__":
   
    log.init("INFO")
    
    threadings = [threading.Thread(target=vk_bot.bot.main.start_bot)]


    for thread in threadings:
        thread.start()
    
    tg_bot.bot.main.start_bot()

    for thread in threadings:
        thread.join()

