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

# convert to lower case
sentence = sentence.lower()
# Replace me with executor
sentence = sentence.replace(' me ', ' snatarajapillai ',1)
# Convert "Delete" to "remove"
sentence = sentence.replace(' delete ', ' remove ',1)
# Convert "Subscribe" to "add"
sentence = sentence.replace(' subscribe ', ' add ',1)
# Convert  "dl" to "DL"  as NLTK identifies smallcase dl as verb
# pay attention not to capitalize 'dl' which is part of any DLname 
# by using space around (' dl ' vs 'dl')
sentence = sentence.replace(' dl ', ' DL ',1)
sentence = sentence.replace(' distributionlist ', ' DL ',1)
sentence = sentence.replace(' distribution list ', ' DL ',1)
#STEP 1 ENDS

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
    SBJ: {<VB.*><PRP|NN.*|VB.*|JJ>+} # ADD X [Get the subject]
    TO: {<TO><DT>?<PRP|NN.*|JJ>+} # Add X TO DL [Get the Object]
    FROM:{<IN><DT>?<PRP|NN.*|JJ>+} # Remove X FROM [Get the Object]
"""
#End of Grammar List

#Step 3 : Parse
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens) 
print(tagged)

#STEP 3.1 Verb Phrase parsing - starts
phraseParser = nltk.RegexpParser(grammar)
result = phraseParser.parse(tagged) 
#result.draw()
for subtree in result.subtrees(filter = lambda t: t.label()=='SBJ'):
        subject = subtree.leaves()
        #Get the Verb
        verbsinSubject = [item for item,tag in subject if tag in ["VB","RB"]]
        SubjectVerb = verbsinSubject
        #Get the Noun
        nounsinSubject = [item for item,tag in subject if tag in ["NN","NNP","NNS","JJ","RB"]]
        output['Subject'] = nounsinSubject 
#Verb Phrase parsing - ends    

#STEP 3.2 Preposition Phrase(FROM) parsing - starts
for subtree in result.subtrees(filter = lambda t: t.label()=='FROM'):
    phrases = subtree.leaves() 
    for leaf in phrases: 
        # check for phrases starting with "as"
        asPhrase = [item for item,tag in phrases if item.upper() in ["AS"]]
        if(len(asPhrase) > 0):
            nounsinAsPhrase = [item for item,tag in phrases if tag in ["NN","NNP","NNS","JJ"]]
            output['Role'] = nounsinAsPhrase
              
        # check for phrases starting with "from"
        fromPhrase = [item for item,tag in phrases if item.upper() in ["FROM","OF"]]
        if(len(fromPhrase) > 0):
            nounsinFromPhrase = [item for item,tag in phrases if tag in ["NN","NNP","NNS","JJ"]]
            output['ObjectNoun'] = nounsinFromPhrase
             
#Preposition Phrase parsing - ends

#STEP 3.3 Preposition Phrase(TO followed by verb) parsing - starts
for subtree in result.subtrees(filter = lambda t: t.label()=='TO'):
    phrase = subtree.leaves()
    nounsinToPhrase = [item for item,tag in phrase if tag in ["NN","NNP","NNS","VB","JJ"]]
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