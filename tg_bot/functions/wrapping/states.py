



class States: 

    def __init__(self) -> None:
        self.isActive = False

    def start(self, VK, TG, cycle, timer):

        self.isActive = True
        self.VK = VK 
        self.TG = TG
        self.cycle = cycle
        self.timer = timer

    def stop(self):
        self.isActive = False