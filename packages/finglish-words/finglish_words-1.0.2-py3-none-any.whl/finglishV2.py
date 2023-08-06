from persion_and_english_letters import letters_dict
from check_style import Style_Check
import re
class Finglish(Style_Check):
    
    def __init__(self):
        
        self.letters_dict = letters_dict
        
    
    def make_finglish_words(self,word):
        
        words = list(word)
        
        
        new_list = []
        counter = 0
        for word in words:
            
            cond ,res = self.check_style(word,counter)
            
            
            if cond:
                res = res
            else :
                try:
                    res = self.letters_dict[word]
                except:
                    pass
            new_list.append(res)
           
            
            
            counter +=1
        final_word = "".join(new_list)
       
        return final_word
    def make_finglish_sentences(self,sentence):
        sentence = sentence.split(' ')
        
       
        sentencelist = []
        for word in sentence:
            try:
                
                res = self.make_finglish_words(word)
                sentencelist.append(res)
            except Exception as e:
                res = word
                sentencelist.append(res)
               
        final_output = " ".join(sentencelist)
        final_output = re.sub("\n","",final_output)
        return final_output