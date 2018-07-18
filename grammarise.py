import sys,nltk,numpy,json
import math
from collections import Counter

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
        print(grammar_tag)
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

def build_vector(input_iterable_sentence,corpora_word_list):
    counter = Counter(input_iterable_sentence)
    vector = [counter[k] for k in corpora_word_list]
    return vector

def cosim(v1, v2):
    print(v1)
    print(v2)
    dot_product = sum(n1 * n2 for n1, n2 in zip(v1, v2) )
    magnitude1 = math.sqrt(sum(n ** 2 for n in v1))
    magnitude2 = math.sqrt(sum(n ** 2 for n in v2))
    return dot_product / (magnitude1 * magnitude2)
# End of functions


# Read Input
input_sentence =  read_input()

# Build Vocabulary for first time
if input_sentence == "0":
    corpora_word_list =[]
    file = open("corpora\corpora.txt", "r") 
    corpora = file.readlines()
    
    for sentence in corpora:
        sentence_nouns_masked = remove_noun(sentence)
        words = nltk.word_tokenize(sentence_nouns_masked)  
        corpora_word_list.extend(words)
    print(sorted(list(set(corpora_word_list))))
    corpora_word_list = sorted(list(set(corpora_word_list)))
    
    #Write the word list to text file
    with open("words.txt", "w") as text_file:
        text_file.write(json.dumps(corpora_word_list)) 

    #Get vectors for sentences and write it to text file
    with open("vector.txt", "w") as text_file:
         for sentence in corpora:
             v = build_vector(sentence.split(),corpora_word_list)        
             text_file.write(json.dumps(v).strip('[').strip(']'))
             text_file.write('\n')


# Analyse the input sentence with Training Vectors

#Read the existing Vector File
else:
    with open('vector.txt', 'r') as vectorFile:
        vocab_vector = numpy.loadtxt("vector.txt",dtype='int',delimiter=',')    

    with open('words.txt') as corpora_word_list:
        word_list = json.load(corpora_word_list)    
# Calculate Cosine difference/similarity 
    for idx,vec in enumerate(vocab_vector):
        input_vec = build_vector(input_sentence.split(),word_list);
        print('{}.{}'.format(idx+1, cosim(input_vec, vec)))
         


    