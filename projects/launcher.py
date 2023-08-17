import repost
import repostbychelyaba
import threading
import parser_bot

def startkzn():
    repost.main()

def startchlb():
    repostbychelyaba.main()

def startparserbot():
    parser_bot.main()
      

if __name__=="__main__":
   
     t1 = threading.Thread(target=startkzn)
     t2 = threading.Thread(target=startchlb)
     #t3 = threading.Thread(target=startparserbot)
     

     t1.start()
     t2.start()
     #t3.start()
     startparserbot()
     
     t1.join()
     t2.join()
     #t3.join()
   

