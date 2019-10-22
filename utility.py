import os
import json

# Deletes file if file exists
def deleteFile():
    fileNames = ["tokenized.json", "DocumentIDFile.json", "TermIDFile.json", "indexList.json", "InvertedIndex.json", "stats.txt"]
    for fileName in fileNames:
        if os.path.exists(fileName):
            os.remove(fileName)
        else:
            print("Cannot delete the file. File does not exists")

# Writes to the Json file
def writeToJson(input, fileName):
    with open(fileName, 'w') as jsonFile:
        json.dump(input, jsonFile, indent=4)

# Read from the Json file
def readJsonFile(fileName):
    data = {}
    with open(fileName, 'r') as jsonFile:
        data = json.load(jsonFile)
    return data

# returns total size of the three index files
def getTotalIndexSize():
    docInfo = os.stat("DocumentIDFile.json")
    termInfo = os.stat("TermIDFile.json")
    invertedInfo = os.stat("InvertedIndex.json")

    totalIndexSize = docInfo.st_size + termInfo.st_size + invertedInfo.st_size

    return totalIndexSize

# Writes total file size, total number of tokens, total number of unique tokens,
# total index size and ratio of total index size to total file size to
# stats.txt file
def writeToStats(totalFileSize, totalNumTokens, totalNumUniqTokens):
    totalIndexSize = getTotalIndexSize()
    stats = [f"Total file size of all the input files (in bytes): {totalFileSize}\n",
    f"Total number of tokens across all input files: {totalNumTokens}\n",
    f"Total number of unique tokens across all input files:{totalNumUniqTokens}\n",
    f"Total index size, that is total size of the three index files (in bytes): {totalIndexSize}\n",
    f"Ratio of total index size to total file size is {totalIndexSize}:{totalFileSize}"]

    with open('stats.txt', 'a') as statsFile:
        for stat in stats:
            statsFile.write(stat)
