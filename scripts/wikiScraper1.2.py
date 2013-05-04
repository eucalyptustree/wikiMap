import csv, re, cStringIO, codecs, string, json
from pattern.web import URL, DOM, plaintext, strip_between
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
import datetime, sys


#Unicode writer from previous assignments
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def getLatLon(ipAddress):
    ipUrl = URL("http://freegeoip.net/json/"+ipAddress)
    ipDom = DOM(ipUrl.download(cached=False))
    ipDict = json.loads(ipDom.content)
    #print ipDict
    return ipDict


def getRandomHistoryDOM(language):
    url = URL("http://"+language+".wikipedia.org/wiki/Special:Random")
    #Gets the url only of the page this redirects to
    redirectUrl = url.redirect
    try:
        #Grab the name of the wikipedia article from the url
        urlComponents = string.split(redirectUrl, '/')
    except AttributeError:
        #Use some recursion if we encounter a page with no history, or some other error
        return getRandomHistoryDOM(language)

    #Get the history section of the article
    redirectUrl = "http://"+language+".wikipedia.org/w/index.php?title="+urlComponents[4]+"&action=history"
    print "Current article is: " +str(urlComponents[4])
    #print redirectUrl
    url = URL(redirectUrl);
    dom = DOM(url.download(cached=False))
    try:
        historyList = dom.by_id("pagehistory").by_tag("li")
        return historyList, urlComponents[4]
    except AttributeError:
        #Use some recursion if we encounter a page with no history, or some other error
        dom = getRandomHistoryDOM(language)

    return getRandomHistoryDOM(language)
    

#We don't need an especially strong validation test here - if it looks like an IP address, it will do
def isIpAddress(ipAddress):
    if len(string.split(ipAddress, ':')) == 8:
        #ipv6 address? I'll be surprised if I see any of these
        return False

    ipAddress = string.split(ipAddress, '.')
    if len(ipAddress) == 4:
        for oneByte in ipAddress:
            if not oneByte.isdigit():
                return False
        return True
    return False


#Different langauges have differnet formats for dates -- because we're only *really* looking for the time, it does make sense to just
#grab all phrases with the format "xx:xx" (where x is a digit)
def formatDate(dateStr):
    dateComponents = string.split(dateStr, ' ')
    for dateComponent in dateComponents:
        #Some country's dates use a '.' instead of a ':'
        dateComponent = string.replace(dateComponent, '.', ':')
        dateComponent = string.strip(dateComponent, ',')
        hrMinute = string.split(dateComponent, ':')
        #print hrMinute
        if len(hrMinute) == 2:
            #May be a time, test further
            if (len(hrMinute[0])== 2) and (len(hrMinute[1]) == 2):
                return str(dateComponent)

        #UNCOMMENT FOR pt LANGUAGE
        #hrMinutePt = string.split(dateComponent, 'h')
        #if len(hrMinutePt[0]) == 2 and len(hrMinutePt[1]) == 5:
        #    hrMinutePt[1] = string.replace(hrMinutePt[1], 'min', '')
        #    if len(hrMinutePt[1]) == 2:
        #        return hrMinutePt[0]+':'+hrMinutePt[1]


# Need two different writers -- one for titles, another for scores





#list of all languages we will be scraping
#languageList = ['en', 'ru', 'pl', 'ja', 'sv', 'pt', 'zh', 'vi', 'uk', 'ca', 'no', 'fi', 'fa', 'cs', 'hu', 'ko', 'ro', 'ceb', 'ar', 'id', 'tr', 'ms', 'sk', 'sr', 'eo', 'da', 'lt', 'eu', 'bg', 'he', 'war', 'sl', 'hr', 'vo', 'et', 'hi', 'gl', 'nn', 'az', 'la', 'el', 'uz', 'th', 'sh', 'ka', 'oc', 'new', 'mk', 'tl', 'pms', 'be', 'ht', 'ta', 'te', 'be-x-old', 'lv', 'br', 'mg', 'sq', 'hy', 'jv', 'cy', 'mr', 'lb', 'is', 'bs', 'my', 'yo', 'ba', 'an', 'ml', 'lmo', 'af', 'fy', 'pnb', 'bn', 'sw', 'roa-rup', 'bpy', 'io', 'ky', 'scn', 'ne', 'gu', 'zh-yue', 'nds', 'ku', 'ga', 'ast', 'qu', 'tt', 'cv', 'ia', 'bug', 'nap', 'als', 'bat-smg', 'sco', 'map-bms', 'kn', 'wa', 'ckb', 'am', 'gd', 'hif', 'zh-min', 'tg', 'mzn']
orderedLanguages = ['en','de','fr','nl','it','ru','es','pl','sv','ja']#,'pt','zh','vi','uk','ca','no','ceb','fi','war','fa','cs','hu','ko','ro','ar','tr','id','kk','ms','sr','sk','eo','da','lt','eu','bg','he','sl','hr','vo','et','hi','uz','gl','nn','simple','az','la','el','th','sh','ka','oc','new','mk','tl','pms','be','ht','ta','te','be-x-old','lv','br','mg','sq','hy','jv','cy','mr','lb','is','tt','bs','my','yo','ba','ml','an','lmo','af','fy','pnb','bn','sw','bpy','io','ky','ur','scn','ne','gu','zh-yue','nds','ku','ga','ast','qu','su','cv','sco','ia','als','bug','nap','bat-smg','map-bms','kn']
culledLanguages = ['en','de','fr','nl','it','ru','es','pl','sv','ja','zh','vi','uk','ca','no','ceb','fi','war','fa','cs','hu','ko','ro','ar','tr','id','kk','ms','sr','sk','eo','da','lt','eu','bg','he','sl','hr','vo','et','hi','uz','gl','nn','simple','az','la','el','th','sh','ka','oc','new','mk','tl','pms','be','ht','ta','te','be-x-old','lv','br','mg','sq','hy','jv','cy','mr','lb','is','tt','bs','my','yo','ba','ml','an','lmo','af','fy','pnb','bn','sw','bpy','io','ky','ur','scn','ne','gu','zh-yue','nds','ku','ga','ast','qu','su','cv','sco','ia','als','bug','nap','bat-smg','map-bms','kn']

languages = orderedLanguages
countPerIter = 100


##output = open("wikipedia.csv", "wb")

'''
file opening within for language loop.
# Store a new file each time the scraper is started. This makes it easier to re-start when
# errors occur, and also allows us to operate the scraper in parallel.
##timeNowStr=string.replace(string.replace((str(datetime.datetime.now()).split(".")[0]),":","-")," ","-")
##filename = "wikipedia"+timeNowStr+".csv"
##output = open(filename, "wb")
'''


## removed the header row, to make combining multiple output files easier
#print len(languages)
#writer.writerow(['language', 'time', 'ip address', 'latitude', 'longitude', 'city', 'country', 'article']);

#initialize all the variables used in the scraper.
curArticle, username, date, time = '','','',''

def scrape():
    curArticle, username, date, time = '','','',''
    for language in languages:
        try:
            print "Current language is: "+language
            ipAddresses = 0   # reset ip counter
            # Store a new file each time the scraper is started. This makes it easier to re-start when
            # errors occur, and also allows us to operate the scraper in parallel.
            timeNowStr=string.replace(string.replace((str(datetime.datetime.now()).split(".")[0]),":","-")," ","-")
            filename = language+"-wikipedia.csv"#+timeNowStr+".csv"
            try:
                output = open(filename, "ab")
            except:
                output = open(filename, "wb")
            writer = UnicodeWriter(output)

            #reset everything
            #articles = 0
            #records = 0
            while ipAddresses < countPerIter:
                #ipAddresses+=1
                #While we're collecting IP addresses, get a new page DOM
                ## added curArticle capture from getRandomHistoryDOM --Y
                historyList, curArticle = getRandomHistoryDOM(language)
                #articles += 1
                #print historyList
                #Occasionally something messes up, and we have to make sure there are actually records there
                for history in historyList:
                    #records += 1
                    #Skip repeating usernames
                    if len(history.by_class("mw-userlink")) > 0:
                        if history.by_class("mw-userlink")[0].content != username:
                            username = history.by_class("mw-userlink")[0].content
                            if isIpAddress(username):
                                #print history.by_class("mw-userlink")[0].content
                                if len(history.by_class("mw-changeslist-date")) < 1:
                                    #print "ERROR!"
                                    #print history.by_class("mw-changeslist-date").content
                                    #This is likely a deleted history -- we should still count it, as someone put forth the effort to make the edit at some point.
                                    date = history.by_class("history-deleted")[0].content
                                else:
                                    date = history.by_class("mw-changeslist-date")[0].content
                                time = formatDate(date)
                                latLon = getLatLon(username)

                                #print language+": "+time+" "+username+" (is ipAddress)"
                                latLon = getLatLon(username)
                                ## added curArticle column to recordRow
                                recordRow = [language, time, username, str(latLon["latitude"]), str(latLon["longitude"]), latLon["city"], latLon["country_name"], curArticle]
                                ipAddresses += 1
                                writer.writerow(recordRow);
                                print "Number of IP addresses: "+str(ipAddresses)
                    else:
                        pass
                        #print "There was an error. No histories found"
        except:
            output.close()
            errors = ["<class 'pattern.web.URLTimeout'>", "<type 'exceptions.KeyboardInterrupt'>", "<type 'exceptions.RuntimeError'>"]
            if str(sys.exc_info()[0]) not in errors:
                
                timeNowStr=string.replace(string.replace((str(datetime.datetime.now()).split(".")[0]),":","-")," ","-")
                fn = "error"+str(timeNowStr)+".txt"
                e= open(fn, 'wb')
                e.write('Error was:'+str(sys.exc_info()[0])+'\n')

                e.write('Error occured at '+timeNowStr+'\n')
                e.write('Language:'+language+'\n')
                e.write('Article:'+str(curArticle)+'\n')
                try:
                    e.write('Date:'+str(date)+'\n')
                    e.write('Time:'+str(time)+'\n')
                except:
                    e.write('date/time missing, sorry.')
                e.close()
            print "Scraper was stopped."

        output.close()
    scrape()
print "Languages to be scraped are:"
print languages

scrape()
