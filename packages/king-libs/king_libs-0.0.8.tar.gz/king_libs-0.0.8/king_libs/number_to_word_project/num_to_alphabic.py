import json
import os
import random
from .basic_number import basic_number
class Ntw:
    def __init__(self):
        
        
        self.hezar = "هزار"
        # with open('number_to_word_project/basic_number.json','r',encoding='utf8') as basic:
        #     data = json.load(basic)
        self.data = basic_number
    def level2(self,number):
        
        
        
        
        if (0 < number < 20 ):
            
            main = self.data.get(str(number))
            return main
            
        
        elif (19 < number < 100 ) :
            if (str(number)[-1]!= "0") :
                first = self.data.get(str(number)[0]+"0")
                second = self.data.get(str(number)[1])
                main = first+" "+"و"+" "+second
                return main
                
            else:
             
                main = self.data.get(str(number))
                return main
        
    def level3(self,number):
        if "".join(str(number)[1:]) == "00":
            sadgan = self.data.get(str(number))
            return sadgan
        elif str(number)[-1]== "0":
            sadgan = self.data.get(str(number)[0]+"00")
            dahgan = "".join(str(number)[1:])
            
            dahgan = self.level2(int(dahgan))
            main = sadgan +" "+"و"+" "+ dahgan
            return main
            
        else:
            
            sadgan = self.data.get(str(number)[0]+"00")
            dahgan = "".join(str(number)[1:])
            dahgan = self.level2(int(dahgan))
            
            main = sadgan +" "+ dahgan
            return main
    
       
    

            
                    
                            
    def level4(self,number):
        
        num_len = len(str(number)[:])
        zeros_count = str(number)[:].count('0')
        if num_len - zeros_count == 1:
            hezargan = self.data.get(str(number)[0])+" "+self.hezar
            main = hezargan
            return main
        else:
        
            for ind,num in enumerate(str(number)):
                
                if ind > 0:
                    
                    if num != "0":
                        if ind == 1:
                            hezargan = self.data.get(str(number)[0])+" "+self.hezar
                            sadgan = self.level3(int(str(number)[ind:]))
                            main = f"{hezargan} و {sadgan}"
                            return main
                        else:
                            hezargan = self.data.get(str(number)[0])+" "+self.hezar
                            dahgan = self.level2(int(str(number)[ind:]))
                            main = f"{hezargan} و {dahgan}"
                            
                            return main
                            
                            
                        break
                        
                    
    def level5(self,number) :
        num_len = len(str(number)[:])
        zeros_count = str(number)[:].count('0')
        if num_len - zeros_count == 1:
            dahhezargan = int("".join(str(number)[0:2]))
            hezargan = self.level2(dahhezargan)+" "+self.hezar
            
            main = hezargan
            return main
        
        for ind,num in enumerate(str(number)):
            
            if ind > 1:
                
                if num != "0":
                    if ind == 2:
                        dahhezargan = int("".join(str(number)[0:2]))
                        dahhezargan = self.level2(dahhezargan)+" "+self.hezar
                        sadgan = int(str(number)[ind:])
                        sadgan = self.level3(sadgan)
                        main = f"{dahhezargan} و {sadgan}"
                        
                        return main
                    else:
                        dahhezargan = int("".join(str(number)[0:2]))
                        dahhezargan = self.level2(dahhezargan)+" "+self.hezar
                        dahgan = int(str(number)[ind:])
                        dahgan = self.level2(dahgan)
                        main = f"{dahhezargan} و {dahgan}"
                        return main
                    
                        
                    
                
    def level6(self,number):
        num_len = len(str(number)[:])
        zeros_count = str(number)[:].count('0')
        if num_len - zeros_count == 1:
            sadhezargan = int("".join(str(number)[0:3]))
            sadhezargan = self.level3(sadhezargan)+" "+self.hezar
            
            main = sadhezargan
            return main
        
        else:
            for ind,num in enumerate(str(number)):
                
                if ind > 2 :
                    
                    if num != "0":
                        if ind == 3:
                            sadhezargan = int("".join(str(number)[:3]))
                            sadhezargan = self.level3(sadhezargan) +" "+ self.hezar
                            sadgan = int("".join(str(number)[ind:]))
                            sadgan = self.level3(sadgan)
                            main = f"{sadhezargan} و {sadgan}"
                            return main
                        else:
                            sadhezargan = int("".join(str(number)[:3]))
                            sadhezargan = self.level3(sadhezargan) +" "+ self.hezar
                            dahgan = int(str(number)[ind:])
                            dahgan = self.level2(dahgan)
                            main = f"{sadhezargan} و {dahgan}"
                            return main
                    else:
                        
                        sadhezargan = int("".join(str(number)[:3]))
                        
                        sadhezargan = self.level3(sadhezargan) +" "+ self.hezar
                        sadgan = "".join(str(number)[3:])
                        if sadgan=='000':
                            main = sadhezargan
                            return main
                        
                            
                       
# ntw = Ntw()
# # c = 1
# # for n in range(10):
# #     x = random.randint(100000,1000000)
# #     print(x)
# #     res = ntw.level6(x)
# #     print(res,c)
# #     c+=1
# #     print("~"*30)
# x = int(input("~~~~~~~~~~~~~~~~~> : "))
# # for x in range(1000,10000):
# res = ntw.level6(x)
# # print(x)
# print(res)
# # print('*'*50)


