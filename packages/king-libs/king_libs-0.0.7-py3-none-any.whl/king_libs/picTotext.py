import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
import cv2
import os
import pytesseract
import time
class PicToText: 
    def __init__(self): 
        pass
        
    def ptt(self,pic_name,mode=None,show=True):
        current_path =os.path.join( os.getcwd(),'result.txt')

    
      
        image = cv2.imread(pic_name, 0)
       
        thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        if mode != None:
            data = pytesseract.image_to_string(thresh,config='--psm 6')
            with open(current_path,f'{mode}') as txt:
                txt.write(data.strip())
            if show:
                print(data.strip())
            return data
        else:
            data = pytesseract.image_to_string(thresh,config='--psm 6',lang='')
            with open(current_path,'w') as txt:
                txt.write(data.strip())
            if show:
                print(data)
            return data