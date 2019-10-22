import re
import queue
import time
import urllib3
import sys
import os
from utility import *

# This function list files in the the directory  up to the number of files
# passed in
# Reference: https://realpython.com/working-with-files-in-python/
def getFolderListing(folderName, numberOfFiles):
    count = 1;
    fileNames = []
    with os.scandir(folderName) as entries:
        for entry in entries:
            if (count <= numberOfFiles):
                fileNames.append(entry)
                count += 1
    return fileNames

# This function read files than returns a dictionary of filtered files with
# file name without ".txt" extension as key and the filtered file as values.
# Also calculates and returns the total input file sizes
def fileReader(folderName, fileNames):
    filteredFiles = {}
    fileSize = 0;
    for name in fileNames:
        with open(name, 'r') as file:
            statInfo = os.stat(name)
            fileSize += statInfo.st_size
            marker = name
            filteredPage = filterHtmlTags(file.read())
            filteredFiles[os.path.splitext(marker.name)[0]] = (marker.name, filteredPage)

    return (filteredFiles, fileSize)

# This function filters out html tags and other terms that should not be
# tokenized
def filterHtmlTags(page):
    # Filters out image tags and the contents in it then deletes it
    image = re.compile('<img.*?>')
    # Filters out css tags and contents in it then deletes it
    css = re.compile('<style.*?/style>')
    # Filters out head tag and contents in it then deletes it
    head = re.compile('(?s)<head>.*?</head>')
    # Filters out all html tags then deletes it
    htmlTag = re.compile('<.*?>')
    # Filters out script tags and contens in it then deletes it
    scripts = re.compile('(?s)<script.*?>.*?</script>')
    # Filters out comments then deletes it
    comments = re.compile('(?s)<!--.+?-->')
    # Filters out non ascii then deletes it
    nonAscii = re.compile('[^\x00-\x7F]+')
    # Filters out string that has special character in the middle
    # replace with spcace
    specialCharInMiddle = re.compile('(?:\s|^)(\w+)(?=\s|$)')
    # Filter out special characters replace with space
    specialChar = re.compile('[^A-Za-z0-9\.\']+')
    # Filters out . ', characters then deletes it
    commas = re.compile('[\'\.,]+')

    page = re.sub(head, '', page)
    page = re.sub(scripts, '', page)
    page = re.sub(css, '', page)
    page = re.sub(image, '', page)
    pattern = re.compile(r'<p>(.*)</p>', re.DOTALL)
    matches = pattern.search(page)
    page = matches.group(1)

    page = re.sub(htmlTag, '', page)

    page = re.sub(comments, '', page)
    page = re.sub(nonAscii, '', page)
    page = re.sub(specialCharInMiddle, ' ', page)
    page = re.sub(specialChar, ' ', page)
    page = re.sub(commas, '', page)
    return page

# Tokenizes the filterded files and returns tokens and totalNumber of tokens
# in all of the documents processed
def tokenize(filteredFiles):
    # total number of tokens in all of the documents processed
    totalTokens = 0;
    # dictionary that with DocumentId as key and number of tokens and list of
    # tokens as a values
    tokenizedTerms = {}
    for k in filteredFiles:
        tokens = filteredFiles[k][1].split()
        totalTokens += len(tokens)
        tokenizedTerms[k] = (filteredFiles[k][0], len(tokens), tokens)

    return tokenizedTerms, totalTokens

# A Control function thatruns the program and outputs the tokens
def dataTransformer(folderName, numFilesToProcess):
    # Files to be processed
    fileNames = getFolderListing(folderName, numFilesToProcess)
    # Filterd files and the total size of input files
    filteredFiles, fileSize = fileReader(folderName, fileNames)
    # Tokens and total number of tokens
    output, totalTokens = tokenize(filteredFiles)
    # Save to json file so it can be use later
    writeToJson(output, "tokenized.json")

    # prints file name and the tokens for that file on each line
    for k in output:
        print(f"File Name: {output[k][0]} Number of tokens: {output[k][1]}\n{output[k][2]}")
    return (fileSize, totalTokens)
