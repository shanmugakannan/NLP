import nltk
sentence = "i want to search for DL"
 
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
command =""
user=""
userType=""
dl=""


#verbs = [item for item in tagged if item[1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]]
verbs = [item for item in tagged if item[1] in ["VB"]]
me = [item for item in tagged if item[1] in ["PRP"]]
nouns = [item for item in tagged if item[1] in ["NN","NNP","NNS"]]
to = [item for item in tagged if item[1] in ["TO","OF"]]
print(tagged)
#print('verb',verbs)
#print('me',me)
#print('nouns',nouns)

#Get the command -- First Verb encountered in the sentence
for idx,tag in enumerate(tagged):
    if tag[1] in ["VB"]:
        command = tag[0]
        # slice the remaining sentence and provide it as input for further processing
        afterCommand = tagged[idx+1:]
        break

#Get the Member -- Noun after verb
for idx,tag in enumerate(afterCommand):
    if tag[1] in ["NN","PRP","NNS"]:
        user = tag[0]
        afterSubjectNoun = afterCommand[idx+1:]
        break

#Get the user type member/owner
for idx,tag in enumerate(afterSubjectNoun):
    if tag[1] in ["IN"]:
        if tag[0] in ["as"]:
            afterAsConjuction = afterSubjectNoun[idx+1:]
            for idx,tag in enumerate(afterAsConjuction):
                if tag[1] in ["NN"]:
                    userType = tag[0]
                    afterObjectNoun = afterAsConjuction[idx+1:]
                    break
        else:
            afterObjectNoun  = afterSubjectNoun[idx:]  
    else:
            afterObjectNoun  = afterSubjectNoun[idx:]  
            print(afterObjectNoun)
for idx,tag in enumerate(afterObjectNoun):
    if tag[1] in ["NN","NNP"]:
        dl = tag[0]
        break 
   


print(command)
print(user)
print(userType)
print(dl)
 
