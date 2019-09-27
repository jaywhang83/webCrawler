import urllib.request
import re
import queue
import time

seedUrl = "https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones"


def webCrawler(seedUrl, numPages):
    frontier = queue.Queue()
    frontier.put(seedUrl)

    count = 0
    depth = 1
    temp = {}
    while((not frontier.empty()) and (count < numPages and depth < 5)):
        url = frontier.get()
        print("opening: ", url)
        time.sleep(1)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        # print(resp.info())
        # print(resp.geturl())
        respData = resp.read()
        # print(len(respData))

        paragraphs = re.findall(r'<p>(.*?)</p>',str(respData))
        count += 1
        temp[count] = url
        # aTags = re.findall(r'<a href="(.*?)">',str(paragraphs))
        aTags = re.findall(r'<a href="([^">]+?)"',str(paragraphs))
        print(count)
        # TODO
        # write to the file links and the size
        httpString = "https://en.wikipedia.org"
        wikiLinks = "/wiki/"
        citeNoteStr = "#cite_note"
        exclude = ":"
        for aTag in aTags:
            if citeNoteStr not in aTag and wikiLinks in aTag and exclude not in aTag:
                fullUrl = httpString + aTag
                frontier.put(fullUrl)
            if len(aTags) == 0:
                depth += 1

webCrawler(seedUrl, 1000)
