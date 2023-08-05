from .sadhezar import Dynamic_Num_Detect
from .milion import Milion
from .miliyard import MiliYard
import random
class Mili_Detect(Dynamic_Num_Detect):
    
    def __init__(self):
        super().__init__()
    
    def mili_detect(self,number):
        try:
            
            if number < 999999 :
                result = self.detect(number)
            elif 999999 < number < 1000000000:
                mili = Milion()
                result = mili.milion(number)
            elif 999999999 < number < 1000000000000 :
                mlyard = MiliYard()
                result = mlyard.miliyard(number)
                
            return result
        except Exception as error:
            err = '''your number is out of range
            '''
            print(error)
            return err

# md = Mili_Detect()
# x = int(input("===========> : "))

# # x = random.randint(1,1000000000000)

# res = md.mili_detect(x)

# print(res)
