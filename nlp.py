import nltk
from nltk import Tree

# Capitalizes the word DL as dl is termed as a verb in NLTK
def processWords(sentence):
    term = "dl" #term we want to search for
    words = sentence.split() #split the sentence into individual words
    processed_output=""
    for word in words:
        if word=='dl':
            processed_output = processed_output +' ' + word.upper()
        else:
            processed_output = processed_output  +' ' + word
    return processed_output
# End of Function

#input
sentence = processWords("remove me from the dl list help-distributionlist")

#Grammar List
toGrammar = "NP: {<TO><DT>?<PRP|NN.*><PRP|NN.*><PRP|NN.*>?}" # to noun phrase
fromGrammar = "NP: {<IN><DT>?<PRP|NN.*><PRP|NN.*><PRP|NN.*>?}" # to noun phrase
#End of Grammar List

tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

#1. To Phrase parsing - starts
nounphraseParser = nltk.RegexpParser(toGrammar)
result = nounphraseParser.parse(tagged) 
res = result.subtrees(filter = lambda t: t.label()=='NP')

for subtree in result.subtrees(filter = lambda t: t.label()=='NP'):
    toPhrase = subtree.leaves()
    nouns = [item for item,tag in toPhrase if tag in ["NN","NNP","NNS"]]
    print('To Phrase Found')
    print(nouns)
#To Phrase parsing - ends

#2. From Phrase parsing - starts
nounphraseParser = nltk.RegexpParser(fromGrammar)
result = nounphraseParser.parse(tagged) 
res = result.subtrees(filter = lambda t: t.label()=='NP')

for subtree in result.subtrees(filter = lambda t: t.label()=='NP'):
    toPhrase = subtree.leaves()
    nouns = [item for item,tag in toPhrase if tag in ["NN","NNP","NNS"]]
    print('From Phrase Found')
    print(nouns)
#To Phrase parsing - ends

#result.draw()
