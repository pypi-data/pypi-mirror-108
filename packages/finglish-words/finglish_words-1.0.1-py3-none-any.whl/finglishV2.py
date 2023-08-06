from persion_and_english_letters import letters_dict
class Finglish:
    
    def __init__(self):
        self.letters_dict = letters_dict
        
    def make_finglish_words(self,word):
        # word = 'امیر'
        words = list(word)
        
        new_list = []
        counter = 0
        for w in words:
            if (w=='و' )and (counter==0):
                res = 'va'
            else :
                res = self.letters_dict.get(w)
            
            new_list.append(res)
        final_word = "".join(new_list)
        return final_word
    def make_finglish_sentences(self,sentence):
        sentence = sentence.split(' ')
        sentencelist = []
        for word in sentence:
            try:
                
                res = self.make_finglish_words(word)
                sentencelist.append(res)
            except:
                res = word
                sentencelist.append(res)
        final_output = " ".join(sentencelist)
        return final_output