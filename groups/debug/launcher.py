import pooling_kzn
import threading
import helper_bot

def startkzn():
    pooling_kzn.main()

def startparserbot():
    helper_bot.main()
      

if __name__=="__main__":
   
     t1 = threading.Thread(target=startkzn)
     #t3 = threading.Thread(target=startparserbot)
     

     t1.start()
     #t3.start()
     startparserbot()
     
     t1.join()
     #t3.join()
   

