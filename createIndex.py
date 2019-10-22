from dataTransformer import *
from utility import *
import json
import os

# Runs the dataTransformer program
def getTokens(folderName, numFilesToProcess):
    return dataTransformer(folderName, numFilesToProcess)

# Returns the dictionary that consist of DocumentId as a key and the list of
# tokens as value from the tokenized,json file that was saved from the
# dataTransformer program
def getTermFraquency():
    data = readJsonFile("tokenized.json")
    return data

# Creates and returns a Dictionary that has documentId as key and the document
# name and the number of tokens as a vlues. This dictionary will be use to
# create DoCumentIdFIle
def createDocIds():
    docIds = {}
    input = getTermFraquency()

    for k in input:
        docIds[k] = (input[k][0], input[k][1])
    return docIds

# Creates and returns the unique tokens across all of the documents and
# unique tokens in the each files
def findUniqueTerms(input):
    # Set of unique tokens across all of the documents
    uniqueTerms = set()
    # Dictionary that contains documentId as key and the list of unique Tokens
    # a values
    uniqueTermsPerDoc = {}
    # Total number of unique tokens across all files
    totalUniqueTokens = 0;
    for k in input:
        # Set of unique tokens in each file
        uniqueTermDoc = set(input[k][2])
        uniqueTermsPerDoc[k] = uniqueTermDoc
        # Adds new unqiue tokens to the current unique tokens across all files
        uniqueTerms.update(uniqueTermDoc)

    totalUniqueTokens = len(uniqueTerms)
    return uniqueTerms, uniqueTermsPerDoc, totalUniqueTokens

# Creates a TermIDFile.
def createTermIdFile(uniqueTerms, uniqueTermsPerDoc):
    # Dictionary that will be a used create TermIDFile. Uses term as key and
    # term id and document frequency as values
    termIDfile = {}
    # Dictionary that will be used to create a InvertedIndex. Uses term as a key
    # and the termId and the list of documentIds that containts the term as values
    indexList = {}
    # A id that will be map to the term
    id = 0;
    for term in uniqueTerms:
        id += 1
        # List of docuemntId's that contains a term
        docs = []
        for termlist in uniqueTermsPerDoc:
            if term in uniqueTermsPerDoc[termlist]:
                docs.append(termlist)
        termIDfile[term] = (str(id), len(docs))
        indexList[term] = (str(id), docs)
    
    writeToJson(termIDfile, "TermIDFile.json")
    writeToJson(indexList, "indexList.json")

# Creates a InvertedIndex
def createIndex():
    # Dictionary with term as a key and the termId and the list of documentIds
    # that containts the term as values
    termList = readJsonFile("indexList.json")
    # Dictionary that will be used to create InvertedIndexFile
    invertedIndex = {}
    # A Dictionary that has documentId as a key and the list of tokens in the
    # files as a values
    tokens = getTermFraquency()

    # Ieterate thru all the term in the dictionary
    for k in termList:
        # List to hold the fraquencies of the term in each file
        fraqs = []
        # Iterate thru the document id in the each term
        for docId in termList[k][1]:
            # Get the tokens from the document by documentId and count the
            # number of occurence of the term and save it.
            fraqs.append((docId, tokens[docId][2].count(k)))
        invertedIndex[termList[k][0]] = fraqs

    writeToJson(invertedIndex, 'InvertedIndex.json')

# A Control function that runs the program
def createInvertedIndex(folderName, numFilesToProcess):
    deleteFile()
    totalFileSize, totalNumTokens = getTokens(folderName, numFilesToProcess)
    writeToJson(createDocIds(), 'DocumentIDFile.json')
    uniqueTerms, uniqueTermsPerDoc, totalNumUniqueTokens = findUniqueTerms(getTermFraquency())
    createTermIdFile(uniqueTerms, uniqueTermsPerDoc)
    createIndex()
    # Create and write to the stats.txt
    writeToStats(totalFileSize, totalNumTokens, totalNumUniqueTokens)
