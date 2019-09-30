import urllib.request
import urllib.parse
from urllib.parse import urlparse
import re
import queue
import time
import urllib.robotparser
import urllib3
import certifi
import sys
import os

# This function crawlers the web page 
def crawler(seedUrl, numPages):
    BASE = "https://en.wikipedia.org" 
    # Domain for wikipedia; "en.wikipedia.org"
    DOMAIN = urlparse(BASE).hostname
    AGENT = "*"
    MAX_DEPTH = 5
    frontier = queue.Queue()
    # List of pages sizes
    pageSizes = []
    # List of page contents that is used to check 
    # if the page has been crawled
    contents = []
    # Dictionary of links with count as key
    links = {}
    # Keeps a track of number of page crawled
    count = 0
    depth = 1
    # Number of pages at the current depth
    currentCount = 1
    # Number of pages at the next depth
    nextCount = 0

    frontier.put(seedUrl)
    # Initiating PoolManager instance to make requests
    req = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                        ca_certs=certifi.where())
    # Gets Robots.txt so it can be use to check to see if the url can
    # be crawlered 
    robotTxt = urllib.robotparser.RobotFileParser()
    robotTxt.set_url(urllib.parse.urljoin(BASE, 'robots.txt'))
    robotTxt.read()

    while((not frontier.empty()) and (count < numPages and depth <= MAX_DEPTH)):
        url = frontier.get()
        time.sleep(1)
        """
        Making "GET" request. Redirect is set to True so it can follow
        redirect url
        """
        response = req.request('GET', url, redirect=True)

        """
        When count of page number is equal to number of pages in the 
        current depth then all of the pages in the current depth has
        been crawled so increase the depth by 1. Also number of
        pages in the next depth becomes the currentCount
        """
        if count == currentCount:
            depth += 1
            currentCount += nextCount
            nextCount = 0
        # countDepth(count, currentCount, nextCount, depth)
        """
        Url link is only crawled when response code is 200 and url is
        allow to crawl by robotx.txt, it's wiki link, and it has not been
        crawled
        """
        if response.status == 200 and canCrawlRoboTxt(url, AGENT, robotTxt) and checkDomain(url, DOMAIN):
            resp = response.data
            """
            Grabs all of the <P> tag and the all of the contents inside
            so it can be saved to list. It wiil be used to check if the 
            web page has been already crawled
            """
            paragraphs = re.findall(r'<p>(.*?)</p>', str(resp))
            # Checks if the webpage has been already crawled 
            if paragraphs not in contents:
                # If webpage has not been crawled, appends content to 
                # contents list
                contents.append(paragraphs)
                # Url has been crawled so increase the counter 
                count += 1
                # Gets the size of the web page crawled
                pageSize = len(resp)
                # Adds link to the list of links that have been crawled
                links[count]= url
                # Appends the size of the page to the list of page sizes
                pageSizes.append(pageSize)
                print("url: ", url, "count: ", count, "Depth: ", depth)
                """
                Creates name in format; nnn.txt
                Example: 30.txt
                """
                fileName = f"filesCrawled/{count}.txt"
                # Writes the web page crawled to file 
                fileWritter(fileName, None, None, resp.decode('utf-8'))
                # Scrapes and add url to the frontier
                nextCount = addUrlToQueue(resp, frontier, links, nextCount, BASE)
        else:
            print("Connection failed.")
    return links, pageSizes, depth


"""
Function that checks if url is not external link. If url's domain is 
not "en.wikipedia.org" returns False
"""
def checkDomain(url, domain):
    """
    parses the url
    Example:
    url = https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones
    ParseResult(
        scheme='https', netloc='en.wikipedia.org', 
        path='/wiki/Karen_Sp%C3%A4rck_Jones', 
        params='', query='', fragment='')
    """
    parsed = urlparse(url)
    if parsed.hostname != domain:
        print("Wrong domain. External domain")
        return False
    return True


"""
Checks if the url can be allow to crawl by checking the robots.txt.
If url is not allow to crawl, returns False, otherwise True
"""
def canCrawlRoboTxt(url, agent, robotTxt):
    parsed = urlparse(url)
    if not robotTxt.can_fetch(agent, parsed.path):
        print(f"Robot.txt does not allow crawl {parsed.path}")
        return False
    return True


"""
This function parses for the urls that starts with "/wiki/".
Then it adds urls that does not ends with Main_Page and 
that does not contains ":" to the frontier to be crawl.
The number of the pages for the depth also increases 
"""
def addUrlToQueue(resp, frontier, links, nextCount, base):
    aTags = re.findall(r'href="(\/wiki\/[^\'" >]+)',str(resp))
    excludeMain = "/Main_Page"
    exclude = ":"
    for aTag in aTags:
        if not(aTag.endswith(excludeMain)) and exclude not in aTag:
            fullUrl = urllib.parse.urljoin(base, aTag)
            if fullUrl not in links.values():
                frontier.put(fullUrl)
                nextCount += 1
    return nextCount


"""
This function takes in pagesSizes list and depth. It will calculate 
maximum, minimum, and average page sizes crawled. Once calculated 
function will return maximum, minimum, average page sizes and depth.
"""
def calculateSize(pageSizes, depth):
    stats =[]
    maxSize = f"Maximum size: {max(pageSizes)} bytes"
    minSize = f"Minimum size: {min(pageSizes)} bytes"
    avgSize = f"Average size: {sum(pageSizes) / len(pageSizes)} bytes"
    maxDepth = f"Maximum depth reach: {depth}"
    
    stats.append(maxSize)
    stats.append(minSize)
    stats.append(avgSize)
    stats.append(maxDepth)

    return stats


# Writes a data passed on to the file. 
def fileWritter(fileName, urls=None, stats=None, content=None):
    with open(fileName, 'a') as file:
        if urls is not None and stats is None and content is None:
            for k,v in urls.items():
                file.write(f"{k}: {v}\n")
        elif urls is None and content is None and stats is not None:
            for stat in stats:
                file.write(f"{stat}\n")
        elif urls is None and stats is None and content is not None:
            file.write(f"{content}\n")


# Runs the program 
def startProgram(seedUrl, pageNums):
    urls, pageSizes, depth = crawler(seedUrl, pageNums)
    stats = calculateSize(pageSizes, depth)
    fileNameStats = "stats.txt"
    fileNameUrlsCrawled = "URLsCrawled.txt"
    fileWritter(fileNameStats, None, stats, None)
    fileWritter(fileNameUrlsCrawled, urls)

