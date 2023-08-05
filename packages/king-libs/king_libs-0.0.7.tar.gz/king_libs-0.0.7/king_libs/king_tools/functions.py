from king_libs.sort_val import Sort_dic
from .stop_words import stop_words,stop_words2
import re
sd = Sort_dic()
class Word_counter:
    def __init__(self):
        pass
    def  count_letters(self,subject:str,letter:str):
        counter = 0
        for l in subject:
            if l == letter:
                counter += 1
                
                
        return counter
    def top_used_letter(self,subject:str,count = 5,cond=True):
        words = 'qwertyuiopasdfghjklmnbvcxzQWERTYUIOPLKJHGFDSAZXCVBNM'
        dic = {}
        for w in words:
            counter = 0
            for l in subject:
                if l == w:
                    counter += 1
            dic[w] = counter
            counter = 0
        top_letter = sd.sort_values(dic=dic,rev=cond)
        lst_val = list(top_letter.values())
        counter = 0
        new_top_letter = {}
        for k,v in top_letter.items():
            new_top_letter[k] = v
            counter += 1
            if counter == count:
                break
        
            
            
            
        return new_top_letter

    def count_words(self,subject:str,word:str):
        lst = re.finditer(word,subject)
    
        matches = [w.span() for w in lst]
        count_word = len(matches)
    
        
        
        return count_word , matches
    
    def top_used_words(self,subject:str,count = 5,rev=True,stopwords=False):
        lst_words = [w for w in subject.lower().split(" ")]
        lst_words = list(map(lambda w : re.sub('\n',' ',w),lst_words))
        if not stopwords:
            stpw = self.stop_words()
            clean_lst_words = []
            for w in lst_words:
                
                if (w  not in stpw) and (w not in stop_words2):
                    clean_lst_words.append(w)
            lst_words = list(map(lambda w:re.sub('\s','',w),clean_lst_words))
            lst_words = list(map(lambda w:w.replace('.',''),lst_words))
            lst_words =set (lst_words)
        
        word_dict = {}
        for w in lst_words:
            try: 
                counter, _ = self.count_words(subject,w)
                
                # res = re.finditer(w,subject)
                # ln =len ([ i for i in res])
                word_dict[w] = counter
                
            except:
                pass
        word_dict = sd.sort_values(word_dict,rev=rev)
        c = 0
        last_dict = {}
        for k,w in word_dict.items():
            if c == count:
                break
            last_dict[k] = w
            
            c +=1
        return last_dict
    def stop_words(self):
        
        return stop_words.split('\n')
        
