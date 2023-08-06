class Style_Check:
    
    def __init__(self):
        
        pass
    def check_style(self,word,counter):
        
        if word == 'و':
            if counter == 0:
                res = 'va'
                return True,res
            else:
                return False , word
        elif word == 'ی':
            if counter == 0:
                res = 'y'
                return True,res
            else:
                return False,word
        elif word == 'ن':
            
            if counter == 0:
                res = 'na'
                return True,res
            else:
                return False,word
                
        else:
            return False,word