import nltk,sys,json
from nltk import Tree
import json 

def read_input():
    return sys.argv[1]

#Output variables
output = {}
output['Subject'] = {}
output['ObjectNoun'] = {}

#STEP 0 :Read Input######################################################################################
sentence =  read_input()

#STEP 1 :Pre-process Input######################################################################################

#STEP 1 ENDS
# convert to lower case
sentence = sentence.lower()
# Replace me with executor
sentence = sentence.replace('me', 'snatarajapillai',1)
# Convert "Delete" to "remove"
sentence = sentence.replace('delete', 'remove',1)
# Convert "Subscribe" to "add"
sentence = sentence.replace('subscribe', 'add',1)
# Convert  "dl" to "DL"
sentence = sentence.replace('dl', 'DL',1)
sentence = sentence.replace('distributionlist', 'DL',1)
sentence = sentence.replace('distribution list', 'DL',1)


#STEP 2 :Define grammar for Text Parsing######################################################################################
toGrammar = "NP: {<TO><DT>?<PRP|NN.*>+}" # to noun phrase
fromGrammar = "NP: {<IN><DT>?<PRP|NN.*>+}" # from noun phrase
verbPhraseGrammar = "VBP: {<VB.*><PRP|NN.*>+}" # verb phrase

sampleGrammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
grammar = r"""     
    TO: {<TO><DT>?<PRP|NN.*>+} # to phrase  [To get the object]       
    FROM: {<IN><DT>?<PRP|NN.*>+} # from phrase [To get the object]
    SBJ: {<VB.*><PRP|NN.*|VB.*>+} # verb phrase [To get the subject]
"""
#End of Grammar List

#Step 3 : Parse
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens) 

#STEP 3.1 Verb Phrase parsing - starts
phraseParser = nltk.RegexpParser(grammar)
result = phraseParser.parse(tagged) 
#print(result)
#result.draw()
for subtree in result.subtrees(filter = lambda t: t.label()=='SBJ'):
        subject = subtree.leaves()
        #Get the Verb
        verbsinSubject = [item for item,tag in subject if tag in ["VB"]]
        SubjectVerb = verbsinSubject
        #Get the Noun
        nounsinSubject = [item for item,tag in subject if tag in ["NN","NNP","NNS"]]
        output['Subject'] = nounsinSubject 
#Verb Phrase parsing - ends    

 #STEP 3.2 Preposition Phrase(FROM) parsing - starts
for subtree in result.subtrees(filter = lambda t: t.label()=='FROM'):
    phrase = subtree.leaves()
    nounsinToPhrase = [item for item,tag in phrase if tag in ["NN","NNP","NNS"]]
    output['ObjectNoun'] = nounsinToPhrase
#Preposition Phrase parsing - ends

#STEP 3.3 Preposition Phrase(TO followed by verb) parsing - starts
for subtree in result.subtrees(filter = lambda t: t.label()=='TO'):
    phrase = subtree.leaves()
    nounsinToPhrase = [item for item,tag in phrase if tag in ["VB","JJ","NN","NNP","NNS"]]
    output['ObjectNoun'] = nounsinToPhrase
#Preposition Phrase parsing - ends

#STEP 4 :Text Analysis######################################################################################

#Add/Remove Member
synonym_ADD = ["add","include","subscribe"]
synonym_Delete = ["delete","remove","unsubscribe","un-subscribe"]

if len(SubjectVerb) == 0 :
    output['Action']="notfound"
else:
    if SubjectVerb[0].lower() in synonym_ADD:
        output['Action']="addmember"

    if SubjectVerb[0].lower() in synonym_Delete:
        output['Action']="removemember"

#Extract Verbs and Nouns
verbs = [verb[0] for verb in tagged if verb[1] in ["VB"]]
me = [proper[0] for proper in tagged if proper[1] in ["PRP"]]
nouns = [noun[0] for noun in tagged if noun[1] in ["NN","NNP","NNS"]]
#print(verbs)
#print(me)
#print(nouns)

print(json.dumps(output))