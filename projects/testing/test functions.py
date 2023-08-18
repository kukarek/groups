

def main(): #обработчик любого сообщения в тг боте
     
     cycle = 0
     VK = True
     TG = True
     
     s = "start_wraping cycle=3 VK=False T=False"

     if s.find("start_wrapping") != -1:
        
        if s.find("cycle") != -1:
            ss =  s.split('cycle=')[1]
            sss = ss.split(' ')[0]
            cycle = int(sss)
        
        if s.find("VK") != -1:
            ss =  s.split('VK=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               VK = False    

        if s.find("TG") != -1:
            ss =  s.split('TG=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               TG = False

     if s.find("VK") != -1 or s.find("TG") != -1: #если что-то из этого нашел с строке
        
        if s.find("VK") != -1:
            ss =  s.split('VK=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               VK = False   

        if s.find("TG") != -1:
            ss =  s.split('TG=')[1]
            sss = ss.split(' ')[0]
            if sss == "False":
               TG = False

     print(VK)
     input()
if __name__ == '__main__':
    main()
