import sys,nltk
import math
from collections import Counter

#variables
vocab_word_list = []
#functions
def read_input():
    return sys.argv[1]

def cleanse_input(sentence):
    sentence = sentence.replace('subscribe ', ' add ',1)
    sentence = sentence.replace('delete ', ' remove ',1)
    sentence = sentence.replace('myself ', ' me ',1)
    sentence = sentence.replace('my self ', ' me ',1)
    sentence = sentence.replace('my-self ', ' me ',1)
    #Replace "me" with "PRP" proper noun
    sentence = sentence.replace(' me ', ' PRP ',1)
    ignore_words = ['please','pls','a','an','the','dl','dls',"'s",'distributionlist','distribution','list','-']
    input_words = nltk.word_tokenize(sentence)
    #print(input_words)
    cleaned_words = [word.lower() for word in input_words if word.lower() not in ignore_words]
    return cleaned_words

def remove_noun(sentence):
    #Cleanse the input sentence
    words = cleanse_input(sentence)
    output_sentence=""
    for word in words:
        tokens = nltk.word_tokenize(word)
        grammar_tag = nltk.pos_tag(tokens) 
        #print(grammar_tag)
        tagged_word = grammar_tag[0] 
        
        if(tagged_word[1] in ['NN','NNS']):
            output_sentence = output_sentence + ' '
            output_sentence = output_sentence + 'NN'
            output_sentence = output_sentence + ' '
        else:
            output_sentence = output_sentence + ' '
            output_sentence = output_sentence + tagged_word[0]
            output_sentence = output_sentence + ' '
    return output_sentence

def build_vector(iterable):
    counter = Counter(iterable)
    vector = [counter[k] for k in vocab_word_list]
    return vector

def cosim(v1, v2):
    dot_product = sum(n1 * n2 for n1, n2 in zip(v1, v2) )
    magnitude1 = math.sqrt(sum(n ** 2 for n in v1))
    magnitude2 = math.sqrt(sum(n ** 2 for n in v2))
    return dot_product / (magnitude1 * magnitude2)

# End of functions

#STEP 0: Build Vocabulary
file = open("corpora\corpora.txt", "r") 
subscribe_corpora = file.readlines()

  
for sentence in subscribe_corpora:
    sentence_nouns_masked = remove_noun(sentence)
    words = nltk.word_tokenize(sentence_nouns_masked)  
    vocab_word_list.extend(words)

print(sorted(list(set(vocab_word_list))))

#STEP 1: Read Input
#sentence =  read_input()
 



    