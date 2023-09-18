#-------------------------------------------------------------------------
# AUTHOR: Alejandro Mora-Lopez
# FILENAME: search_engine.py
# SPECIFICATION: This is a simple program that outputs the precision and recall of a search engine given a query.
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math

documents = []
labels = []

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])

#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}
newDocs = []

for document in documents:
    words = document.split()
    filtered_words = []
    for word in words:
        if word not in stopWords:
            filtered_words.append(word)
    newDoc = ' '.join(filtered_words)
    newDocs.append(newDoc)
    
documents = newDocs

#Conduct stemming.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

newDocs = []

for i, document in enumerate(documents, start=1):
    words = document.split()
    stemmedWords = []

    for word in words:
        if word in steeming:
            stemmedWords.append(steeming[word])
        else:
            stemmedWords.append(word)
    newDoc = ' '.join(stemmedWords)
    newDocs.append(newDoc)
    print("Stemmed d" + str(i) + ":", newDoc)

documents = newDocs

#Identify the index terms.
#--> add your Python code here

terms = sorted(list(set(' '.join(documents).split())))

#Build the tf-idf term weights matrix.
#--> add your Python code here
docMatrix = []

idf = []
for term in terms:
    count = 0
    for doc in documents:
        if term in doc.split():
            count += 1
    idf.append(math.log(len(documents) / count, 10))

for doc in documents:
    tf = [doc.split().count(term) / len(doc.split()) for term in terms]
    docMatrix.append([tf[i] * idf[i] for i in range(len(tf))])

print(docMatrix)

#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
docScores = []

query = "cat and dogs"
query = ' '.join(word for word in query.split() if word not in stopWords)
query = ' '.join(steeming[word] if word in steeming else word for word in query.split())

print(query)
queryVector = [1 if term in query.split() else 0 for term in terms]

for docVector in docMatrix:
    score = sum([queryVector[i] * docVector[i] for i in range(len(queryVector))])
    docScores.append(score)

print(docScores)

#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
#--> add your Python code here

retrievedDocs = [i for i in range(len(documents)) if docScores[i] >= 0.1]
relevantDocs = [i for i in range(len(documents)) if labels[i] == ' R']
irrelevantDocs = [i for i in range(len(documents)) if labels[i] == ' I']

hits = len(set(retrievedDocs).intersection(set(relevantDocs)))
noise = len(set(retrievedDocs).intersection(set(irrelevantDocs)))
misses = len(set(relevantDocs) - set(retrievedDocs))

precision = hits / (hits + noise)
recall = hits / (hits + misses)

print('Precision:', precision)
print('Recall:', recall)