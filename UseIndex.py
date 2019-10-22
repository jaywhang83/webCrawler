from utility import *
import sys

# Returns termId from the given term
def getTermId(term):
    termId = readJsonFile("TermIDFile.json")[term][0]
    print(termId)
    return termId

# Returns the invertedList from the given termId
def getInvertedList(termId):
    invertedList = readJsonFile("InvertedIndex.json")[termId]
    print(invertedList)
    return invertedList

# Returns the document name from the given document Id
def getDocumentId(docId):
    docName = readJsonFile("DocumentIDFile.json")[docId][0]
    print(docName)
    return docName

# Returns the list of documents the term is in from the term
def getTermInvertedList(term):
    termId = getTermId(term)
    invertedList = getInvertedList(termId)
    docIds = []
    for doc in invertedList:
        docIds.append(doc[0])

    print(docIds)
    return docIds

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
