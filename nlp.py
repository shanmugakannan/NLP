import nltk,sys,json
from nltk import Tree


def read_input():
    return sys.argv[1]

#input
sentence =  read_input()

#Grammar List
#toGrammar = "NP: {<TO><DT>?<PRP|NN.*><PRP|NN.*><PRP|NN.*>?}" # to noun phrase
toGrammar = "NP: {<TO><DT>?<PRP|NN.*>+}" # to noun phrase
fromGrammar = "NP: {<IN><DT>?<PRP|NN.*>+}" # to noun phrase
#End of Grammar List

tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

#0. Extract Verbs and Nouns
verbs = [verb[0] for verb in tagged if verb[1] in ["VB"]]
me = [proper[0] for proper in tagged if proper[1] in ["PRP"]]
nouns = [noun[0] for noun in tagged if noun[1] in ["NN","NNP","NNS"]]
print(verbs)
print(me)
print(nouns)
#1. To Phrase parsing - starts
nounphraseParser = nltk.RegexpParser(toGrammar)
result = nounphraseParser.parse(tagged) 

for subtree in result.subtrees(filter = lambda t: t.label()=='NP'):
    toPhrase = subtree.leaves()
    nouns = [item for item,tag in toPhrase if tag in ["NN","NNP","NNS"]]
    print('To Phrase Found')
    print(nouns)
#To Phrase parsing - ends

#2. From Phrase parsing - starts
nounphraseParser = nltk.RegexpParser(fromGrammar)
result = nounphraseParser.parse(tagged) 

for subtree in result.subtrees(filter = lambda t: t.label()=='NP'):
    toPhrase = subtree.leaves()
    nouns = [item for item,tag in toPhrase if tag in ["NN","NNP","NNS"]]
    print('From Phrase Found')
    print(nouns)
#To Phrase parsing - ends

result.draw()