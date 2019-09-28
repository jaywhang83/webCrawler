import urllib.request
import re
import queue
import time

seedUrl = "https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones"


def webCrawler(seedUrl, numPages):
    frontier = queue.Queue()
    pageSizes = []
    links =[]
    frontier.put(seedUrl)

    count = 0
    depth = 1
    currentCount = 1
    nextCount = 0
    while((not frontier.empty()) and (count < numPages and depth < 5)):
        if count == currentCount:
            depth += 1
            currentCount = nextCount
            nextCount = 0

        url = frontier.get()
        # print("Depth : ", depth, "Count : ", count, "opening: ", url)
        # time.sleep(1)
        
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        # print(resp.info())
        respData = resp.read()
    
        paragraphs = re.findall(r'<p>(.*?)</p>',str(respData))

        count += 1

        links.append(url)
        pageSizes.append(len(respData))

        aTags = re.findall(r'href=[\'"/wiki/]?([^\'": >]+)',str(paragraphs))
        # nextCount += len(aTags)
        # TODO
        # write to the file links and the size
        httpString = "https://en.wikipedia.org"
        wikiLinks = "/wiki/"
        # exclude = ":"
        temp = 0
        for aTag in aTags:
            if aTag.startswith(wikiLinks):
                fullUrl = httpString + aTag
                frontier.put(fullUrl)
                nextCount += 1
                temp += 1
       
        print("count: ", count, "start url: ", url, "depth : ", depth, "number of links : " , temp)
    print(depth)
webCrawler(seedUrl, 1000)
