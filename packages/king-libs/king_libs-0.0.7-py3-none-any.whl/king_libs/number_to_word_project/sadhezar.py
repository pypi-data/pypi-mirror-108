from .num_to_alphabic import Ntw
import random

chng = Ntw()
class Dynamic_Num_Detect:
    
    def __init__(self):
        pass

    def detect(self,number):
        
        if number < 100:
            result = chng.level2(number)
        elif 99 < number < 1000:
            
            result = chng.level3(number)
        elif  999 < number < 10000 :
            
            result = chng.level4(number)
        elif 9999 < number < 100000 :
            result = chng.level5(number)
        elif 99999 < number < 1000000 :
            
            
            result = chng.level6(number)
        
        
        return result

# ml =   Dynamic_Num_Detect()     
# x = int(input('===================> : '))  
# res = ml.detect(x)        
# print(res)
            
