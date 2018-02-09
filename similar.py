import nltk
from nltk.corpus import wordnet
# Let's compare the noun of "ship" and "boat:"
 
w1 = wordnet.synset('delete.v.01') # v here denotes the tag verb
w2 = wordnet.synset('remove.v.01')
print(w1.wup_similarity(w2))