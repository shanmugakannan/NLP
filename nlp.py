import nltk
sentences = ["add me to technology","remove me from dl-pp-etstech","unsubscribe me from dl-pp-tech","create new dl d-pp","add snatarajapillai to dl-pp","delete dl-pp",
"rename dl-pp","subscribe me to dl-pp","subscribe sub-dl to parentdl","make me owner of the dl as the owner has left","give me ownership",
"add snatarajapillai as owner of dl-pp","make snatarajapillai owner of"]
result = ""
grammar = ""

for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    for tag in tagged:
         for i,a in enumerate(tag):
            if i==0:
                result = result + " " + a
            else:
                grammar = grammar + " " + a
    print(result)
    print(grammar)
    result =""
    grammar =""

         

 
