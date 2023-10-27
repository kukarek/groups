from .handler import start_wrapping

class Wrapping: 

    VK = True
    TG = True
    cycle = 0
    timer = 0


    def __init__(self) -> None:
        self.isActive = False

    def start(self) -> bool:

        if self.isActive == False:

            self.isActive = True
            start_wrapping()

            return True
        else:
            return False

    def stop(self):
        
        self.isActive = False

    def change_VK(self):

        if self.VK == True:
            self.VK = False
        else:
            self.VK = True

    def change_TG(self):

        if self.TG == True:
            self.TG = False
        else:
            self.TG = True
    
    def change_cycle(self, cycle: int):

        self.cycle = cycle

    def change_timer(self, timer: int):

        self.timer = timer

    def status(self):

        if self.isActive:
            return f"VK = {self.VK}\n TG = {self.TG}\n cycle = {self.cycle}\n timer = {self.timer}"
        else:
            return f"автонакрутка неактивна"
       

wrapping = Wrapping()