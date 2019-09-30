#! /usr/local/bin/python3 
import sys
from webCrawler import *

# Runs the webCrawler program
def excute_program(seedUrl, numPages):
    startProgram(seedUrl, numPages)

def main():
    seedUrl = ""
    numPages = 0
    if len(sys.argv) != 3:
        print("Please enter seedUrl and numPages in this order")
        sys.exit()
    else:
        seedUrl = sys.argv[1]
        numPages = sys.argv[2]
        excute_program(seedUrl, int(numPages))

if '__main__' == __name__:
    main()