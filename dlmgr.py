import numpy as np
import re
import nltk 
from nltk.tokenize import sent_tokenize, word_tokenize
 
#Pre-process the sentence and extract the words
def extract_words(sentence):
    ignore_words = ['-','?','.','a']
    words = nltk.word_tokenize(sentence)
    cleaned_words = [word for word in words if word not in ignore_words]
    return cleaned_words

def build_vocabulary(sentences):
    word_list = []
    for sentence in sentences:
        sentence = sentence.lower().replace("i'm", 'i am',1).replace("'s", 's',1)
        words = extract_words(sentence)
        word_list.extend(words)
    
    word_list = sorted(list(set(word_list)))
    return word_list

file = open("dlmgr_corpora.txt",encoding="utf8") 
corpora = file.readlines()

vocabulary_vector = build_vocabulary(corpora)
print(vocabulary_vector)