from .executor import Executor


class Wrapping(Executor): 

   
    def start_wrapping(self):

        self.start_wrapp()

   
    def stop_wrapping(self):
        
        self.isActiveWrapping = False


    def status(self) -> str:

        if self.isActiveWrapping:
            
            return "Накрутка активна"
        else:
            return "Накрутка неактивна"
    

       