from .sadhezar import Dynamic_Num_Detect

class Milion(Dynamic_Num_Detect):
    
    def __init__(self):
        super().__init__()
        self.milion_pr = "میلیون"
    def milion(self,number):
        if str(number)[0] != '0':
            
            if len(str(number))==7:
                
                    num_len = len(str(number))
                    zeros_count = str(number)[:].count('0')
                    if num_len - zeros_count == 1:
                        miliongon = self.detect(int(str(number)[0]))+" "+self.milion_pr
                        main = miliongon
                        return main
                    else:
                        miliongon = self.detect(int(str(number)[0]))+" "+self.milion_pr
                        hezargon = self.detect(int(str(number)[1:]))
                        
                        main =  miliongon+" "+"و"+" "+hezargon
                        return main
                        
                            
            elif len(str(number)) == 8:
                
                num_len = len(str(number))
                zeros_count = str(number)[:].count('0')
                if num_len - zeros_count == 1:
                    dah_miliongon = self.detect(int("".join(str(number)[:2]))) +" "+self.milion_pr
                    main = dah_miliongon
                    return main
                else:
                    dah_miliongon = self.detect(int("".join(str(number)[:2]))) +" "+self.milion_pr
                    sadhezargon = self.detect(int(str(number)[2:]))
                    main = dah_miliongon+" "+"و"+" "+sadhezargon
                    return main
            elif len(str(number)) == 9:
                num_len = len(str(number))
                zeros_count = str(number)[:].count('0')
                if num_len - zeros_count == 1:
                    sadmiliongon = self.detect(int("".join(str(number)[:3])))+" "+self.milion_pr
                    main = sadmiliongon
                    return main
                
                else:
                    sadmiliongon = self.detect(int("".join(str(number)[:3])))+" "+self.milion_pr
                    
                   
                    sadhezargon = self.detect(int("".join(str(number)[3:])))
                  
                    main = sadmiliongon+" "+"و"+" "+sadhezargon
                    return main
            
                
# ml =   Milion()     
# x = int(input('===================> : '))  
# res = ml.milion(x)        
# print(res)
                    
