#! /usr/bin/python3
import sys
from createIndex import *

# Runs the createIndex program
def excute_program(folderName, numFilesToProcess):
    createInvertedIndex(folderName, numFilesToProcess)

def main():
    folderName = ""
    numFilesToProcess = 0
    if len(sys.argv) != 3:
        print("Please enter folderName and numFilesToProcess in this order")
        sys.exit()
    else:
        folderName = sys.argv[1] + "/"
        numFilesToProcess = sys.argv[2]
        excute_program(folderName, int(numFilesToProcess))

if '__main__' == __name__:
    main()
