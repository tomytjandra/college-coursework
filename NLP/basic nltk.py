def clear():
    for i in range(5):
        print()

text = "On April 8, 2018, Persekutuan Oikumene (PO) BINUS held an Easter Service to commemorate the resurrection of Jesus Christ. BNEC sent some of its delegations to attend the invitation. It was a great event with all the activities and the warm atmosphere contained the room."

##1. TOKENIZING
from nltk.tokenize import sent_tokenize, word_tokenize
wordList = word_tokenize(text)
sentList = sent_tokenize(text)
print(wordList)
clear()
print(sentList)

##2. STOPWORDS
from nltk.corpus import stopwords
stopList = stopwords.words("english")
wordWithoutStopwords = []
for word in wordList:
    if word not in stopList:
        wordWithoutStopwords.append(word)
clear()
print(wordWithoutStopwords)

##3. STEMMING
from nltk.stem import LancasterStemmer, SnowballStemmer, PorterStemmer
ls = LancasterStemmer()
ss = SnowballStemmer("english")
ps = PorterStemmer()

lsRes = []
ssRes = []
psRes = []

for word in wordList:
    lsRes.append(ls.stem(word))
    ssRes.append(ss.stem(word))
    psRes.append(ps.stem(word))

clear()
print(lsRes)
clear()
print(ssRes)
clear()
print(psRes)

##4. LEMMATIZING
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

wordToBeLemmatized = "Running"
params = ['a','s','r','n','v']
clear()
for param in params:
    print(param + " : " + lemmatizer.lemmatize(wordToBeLemmatized.lower(), param))

##5. POSTAGGING
from nltk.tag import pos_tag
import string

wordWithoutPunc = []
for word in wordList:
    if word not in string.punctuation:
        wordWithoutPunc.append(word)

postag = pos_tag(wordWithoutPunc)

clear()
for word,tag in postag:
    print(word + " : " + tag)

##6. NAME ENTITY RECOGNITION
from nltk.chunk import ne_chunk

ner = ne_chunk(postag)
clear()
print(ner)

choose = ""
while choose == "":
    choose = input("Draw [yes/no]? ")
    if choose not in ["yes","no"]:
        choose = ""
if choose == "yes":
    ner.draw()
    
##7. FREQ DIST
from nltk.probability import FreqDist

fd = FreqDist(wordList)
for word, count in fd.most_common():
    print(word + " : " + str(count))

##BASIC
from nltk.corpus import wordnet

word = "win"
synsetList = wordnet.synsets(word)
woi = synsetList[0]
clear()
print(woi.name())
print(woi.definition())
print(woi.examples())
print(woi.pos())
lemmas = woi.lemmas()
for lemma in lemmas:
    print(lemma.name())

##SYNONYM
synonym = []
for synset in wordnet.synsets(word):
    for lemma in synset.lemmas():
        synonym.append(lemma.name())
synonym = set(synonym)
clear()
print(sorted(synonym))
    
##ANTONYM
antonym = []
for synset in wordnet.synsets(word):
    for lemma in synset.lemmas():
        for anto in lemma.antonyms():
            antonym.append(anto.name())
antonym = set(antonym)
clear()
print(sorted(antonym))

##READ FILE FROM CORPORA
from nltk.corpus import gutenberg
filename = "austen-emma.txt"
#print(gutenberg.raw(filename))

##CLASSIFY MOVIE REVIEWS
##1. IMPORT FOLDER
from nltk.corpus import movie_reviews

##2. TRANSFER TEXT TO LIST (ALLWORDS & DOCS)
n = 30
allWords = []
docs = []
for category in movie_reviews.categories():
    count = 0
    for fileid in movie_reviews.fileids(category):
        wordsInOneFile = []
        for word in movie_reviews.words(fileid):
            wordsInOneFile.append(word.lower())
            allWords.append(word.lower())
        docs.append((wordsInOneFile,category))

        count += 1
        if(count == n):
            break

##3. RANDOM SHUFFLE LIST
import random
random.shuffle(docs)

##4. DEF COLLECT FEATURES
def collectFeatures(wordList):
    wordSet = set(wordList)
    feature = {}
    for word in allWords:
        feature[word] = (word in wordSet)
    return feature

##5. APPLY COLLECT FEATURES
result = []
for (wordList, category) in docs:
    result.append((collectFeatures(wordList), category))    

##6. SPLITTING DATA
splitPoint = int(0.8*2*n)
trainingData = result[:splitPoint]
testingData = result[splitPoint:]

##7. APPLY CLASSIFIER
import nltk
classifier = nltk.NaiveBayesClassifier.train(trainingData)

##8. MODEL EVALUATION
try:
    acc = nltk.classify.accuracy(classifier, testingData)
    clear()
    print("Accuracy: {0:.2f}%".format(acc*100))
    classifier.show_most_informative_features()
except:
    print("No classifier")

##9. WRITE PICKLE
import pickle
file = open("classifier.pickle", "wb")
pickle.dump(classifier, file)
file.close()
    
###0. ADDITIONAL: READ PICKLE, WRITE AND READ STRING FILE
##READ PICKLE
try:
    file = open("classifier.pickle", "rb")
    classifier = pickle.load(file)
    file.close()
    classifier.show_most_informative_features()
except:
    print("No such file")

##WRITE STRING FILE
file = open("test.txt", "w")
file.write("Test\n")
for i in range(10):
    file.write(str(i))
    file.write('\n')
file.close()

##READ STRING FILE
file = open("test.txt", "r")
data = file.read().split()
print(data)
file.close()
