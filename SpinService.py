import pickle
import random
from underthesea import sent_tokenize as sent_tokenize_vi
from underthesea import word_tokenize as word_tokenize_vi

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from random import randint
import nltk.data
import time
from bs4 import BeautifulSoup as soup
from nltk.tokenize import word_tokenize as word_tokenize_en
from nltk.tokenize import sent_tokenize as sent_tokenize_en
import re
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def get_response(input_text,num_return_sequences,num_beams):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = model.generate(**batch,max_length=60,num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text
class SpinService:

    def __init__(self) -> None:
        with open("dataspin.p","rb") as file:
            self.dataspin = pickle.load(file)
        nltk.download('omw-1.4')
        nltk.download('wordnet')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        wordnet.ensure_loaded()


    def spin_paragraph(self,p_paragraph1,keyword):
        p_paragraph = [str(t) if not re.match(r'<[^>]+>', str(t)) else str(t) for t in p_paragraph1.contents]
        word_splits = []
        try:
            for i in p_paragraph:
                if not re.match(r'<[^>]+>', i):
                    word_splits  = word_splits + word_tokenize_vi(i)
                else:
                    word_splits  = word_splits.append(i)
                    if  re.match(r'<img [^>]+>', i):
                        word_splits  = word_splits.append("<br>")


            if(word_splits!=None):
                for index_word in range(len(word_splits)):
                    if word_splits[index_word] in self.dataspin and word_splits[index_word].lower() not in keyword.lower():
                        word_splits[index_word] = random.choice(self.dataspin[word_splits[index_word]])
                paragraph = " ".join(word_splits)
                paragraph = soup(paragraph,"html.parser")

                return paragraph
            else:
                return p_paragraph1
        except:
            return p_paragraph1


    def spin_paragraph_en(self,p_paragraph1,keyword):

        p_paragraph = [str(t) if not re.match(r'<[^>]+>', str(t)) else str(t) for t in p_paragraph1.contents]

        output = ""

        # Get the list of words from the entire text
        # try:
        words = []
        for i in p_paragraph:
            if i!=None:
                if not re.match(r'<[^>]+>', i) and i.lower() not in keyword.lower():
                    try:
                        num_beams = 10
                        num_return_sequences = 1
                        iii = ""
                        for jj in i.split("."):
                            if len(jj)>6:
                                jja  = get_response(jj,num_return_sequences,num_beams)[0]
                                iii = iii  + jja + " "

                        i = iii
                        print(i)
                    except Exception as e:
                        print(e)
                    try:
                        words  = words + word_tokenize_en(i)
                    except:
                        pass
                else:
                    words  = words + [i]
        #except:
        # except Exception as e:
        #     print(e)
        #     return p_paragraph1

        if words!=None:
            if len(words)>0:
                tagged = nltk.pos_tag(words)
            for i in range(0,len(words)):
                replacements = []
                if (tagged[i][1] == 'NN' or tagged[i][1] == 'JJ' or tagged[i][1] == 'RB') and not re.match(r'<[^>]+>', words[i]):
                    try:
                        for syn in wordnet.synsets(words[i]):     
    
                    
                            word_type = tagged[i][1][0].lower()
                            if syn.name().find("."+word_type+"."):
                                # extract the word only
                                r = syn.name()[0:syn.name().find(".")]
                                replacements.append(r)

                    except Exception as e:
                        pass

                if len(replacements) > 0:
                    # Choose a random replacement
                    replacement = replacements[randint(0,len(replacements)-1)]
                    output = output + " " + replacement.replace("_"," ")
                else:
                    # If no replacement could be found, then just use the
                    # original word
                    output = output + " " + words[i]
        else:
            return p_paragraph1
        output = soup(output,"html.parser")
        return output
    def spin_title_vi(self,p_paragraph1,keyword):
        aaa = word_tokenize_vi(p_paragraph1)

        try:
            word_splits = aaa
            if(word_splits!=None):
                for index_word in range(len(word_splits)):
                    if word_splits[index_word] in self.dataspin and word_splits[index_word].lower() not in keyword:
                        word_splits[index_word] = random.choice(self.dataspin[word_splits[index_word]])
                paragraph = " ".join(word_splits)
                paragraph
                return paragraph
            else:
                return p_paragraph1
        except:
            return p_paragraph1


    def spin_title_en(self,p_paragraph1,keyword):
        aaa = word_tokenize_en(p_paragraph1)

        output = ""

        # Get the list of words from the entire text
        try:
            words = aaa
        except:
            return p_paragraph1

        if words!=None:
            if len(words)>0:
                tagged = nltk.pos_tag(words)
            for i in range(0,len(words)):
                replacements = []
                if (tagged[i][1] == 'NN' or tagged[i][1] == 'JJ' or tagged[i][1] == 'RB') and not re.match(r'<[^>]+>', words[i] and words[i].lower() not in keyword.lower()):
                    try:
                        for syn in wordnet.synsets(words[i]):     
    
                    
                            word_type = tagged[i][1][0].lower()
                            if syn.name().find("."+word_type+"."):
                                # extract the word only
                                r = syn.name()[0:syn.name().find(".")]
                                replacements.append(r)

                    except Exception as e:
                        pass

                if len(replacements) > 0:
                    # Choose a random replacement
                    replacement = replacements[randint(0,len(replacements)-1)]
                    output = output + " " + replacement.replace("_"," ")
                else:
                    # If no replacement could be found, then just use the
                    # original word
                    output = output + " " + words[i]
        else:
            return p_paragraph1
        return output