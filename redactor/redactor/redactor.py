# redactor.py
from . import main
from . import unredactor

def redactNames(currInputFile):
    countNames = 0
    currDoc = currInputFile
    stop = stopwords.words('english')

    # find the names
    names = []

    strInput = ' '.join([i for i in currInputFile.split() if i not in stop])
    sentences = nltk.sent_tokenize(strInput)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    #names.append(' '.join([c[0] for c in chunk]))
                    name = ' '.join([c[0] for c in chunk])
                    names.append(name)
    #print ("names: ", names)

    # redacting the names
    for i in names:
        newSentence = ""
        for j in word_tokenize(i):
            redacted = u"\u2588"*len(j)
            redacted +=" "
            newSentence += redacted
        newSentence = newSentence[:-1]
        currDoc = currDoc.replace(i, redacted)
    #print(names)
    # total name redacted    
    countNames = len(names)
    #return textWithRedactedName
    #result = [currDoc, countNames]
    return currDoc, countNames

def get_entity_names(text):
    # store all the person names from entity
    names = []
    """Prints the entity inside of the text."""
    for sent in sent_tokenize(text):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                # store the name from chuck leaves                
                name = ' '.join(c[0] for c in chunk.leaves())
                #for leaf in chunk.leaves():
                #    name += leaf[0]
                #    name += " "
                names.append(name)
    
    # redacting the names
    for i in names:
        newSentence = ""
        for j in word_tokenize(i):
            redacted = u"\u2588"*len(j)
            redacted +=" "
            newSentence += redacted
        newSentence = newSentence[:-1]
        currDoc = currDoc.replace(i, redacted)
    #print(names)
    # total name redacted    
    countNames = len(names)
    #return textWithRedactedName
    #result = [currDoc, countNames]
    return currDoc, countNames

    # return all the names
    return names

def doextraction(glob_text):
    """Get all the files from the given glob and pass them to the extractor."""
    for thefile in glob.glob(glob_text):
        with io.open(thefile, 'r', encoding='utf-8') as file:
            text = file.read()
            get_entity(text)