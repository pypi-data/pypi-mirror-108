from .sadhezar import Dynamic_Num_Detect
from .milion import Milion

class MiliYard(Milion):
    
    def __init__(self):
        super().__init__()
        self.miliyard_pr = "میلیارد"
    def miliyard(self,number):
        if str(number)[0] !='0':
            if len(str(number))==10:
                num_len = len(str(number))
                zeros_count = str(number)[:].count('0')
                if num_len - zeros_count == 1:
                    miliyardgon = self.detect(int(str(number)[0]))+" "+self.miliyard_pr
                    main = miliyardgon
                    return main
                else:
                    miliyardgon = self.detect(int(str(number)[0]))+" "+self.miliyard_pr
                    miliongon = self.milion(int("".join(str(number)[1:])))
                    main = miliyardgon+" "+"و"+" "+miliongon
                    return main
            elif len(str(number)) == 11:
                num_len = len(str(number))
                zeros_count = str(number)[:].count('0')
                if num_len - zeros_count == 1:
                    dahmiliyardgon = self.detect(int("".join(str(number)[:2])))+" "+self.miliyard_pr
                    main = dahmiliyardgon
                    return main
                else:
                    dahmiliyardgon = self.detect(int("".join(str(number)[:2])))+" "+self.miliyard_pr
                    sadmiliongon = self.milion(int("".join(str(number)[2:])))
                    main = dahmiliyardgon+" "+"و"+" "+sadmiliongon
                    return main
            elif len(str(number)) == 12:
                num_len = len(str(number))
                zeros_count = str(number)[:].count('0')
                if num_len - zeros_count == 1:
                    sadmiliyardgon = self.detect(int("".join(str(number)[:3])))+" "+self.miliyard_pr
                    main = sadmiliyardgon
                    return main
                    
                    
                else:
                    sadmiliyardgon = self.detect(int("".join(str(number)[:3])))+" "+self.miliyard_pr
                    print(sadmiliyardgon)
                    
                    sadmiliongon = self.milion(int("".join(str(number)[3:])))
                    
                    main = sadmiliyardgon+" "+"و"+" "+sadmiliongon
                    return main
                
                    
# mly = MiliYard()
# x = int(input("====================> : "))
# res = mly.miliyard(x)
# print(res)