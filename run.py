import threading
import modules.vk_bot.bot.main
import modules.tg_bot.bot.main

import log

if __name__=="__main__":
   
    log.init("DEBUG")
    
    threadings = [threading.Thread(target = modules.vk_bot.bot.main.start_bot)]


    for thread in threadings:
        thread.start()
    
    modules.tg_bot.bot.main.start_bot()

    for thread in threadings:
        thread.join()

