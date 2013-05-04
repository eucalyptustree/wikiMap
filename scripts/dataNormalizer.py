
##def lineCount(fname):
##    count = 0
##    f = open(fname, 'rb')
##    for l in f:
##        count+=1
##    #print count
##    return count
        
orderedLanguages = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs','hu','fa','ko','ro','ar','tr','id','kk','ms','sr','sk','eo','da','lt','eu','bg','he','sl','hr','vo','et','hi','uz','gl','nn','simple','az','la','el','th','sh','ka','oc','new','mk','tl','pms','be','ht','ta','te','be-x-old','lv','br','mg','sq','hy','jv','cy','mr','lb','is','tt','bs','my','yo','ba','ml','an','lmo','af','fy','pnb','bn','sw','bpy','io','ky','ur','scn','ne','gu','zh-yue','nds','ku','ga','ast','qu','su','cv','sco','ia','als','bug','nap','bat-smg','map-bms','kn']

languages20 = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs']
languagesCounts = [112264,22575,16980,6926,11675,11549,13116,6777,4105,8920,6659,5011,2071,2345,2191,2357,431,2544,468,1919]

countTargets = {}

for l in orderedLanguages:
    countTargets[l] = 0

for i in range(len(languages20)):
    countTargets[languages20[i]]=languagesCounts[i]


##print countTargets
for l in languages20:
    print l,countTargets[l]
raw_input()
    
countDict={}
L = languages20
countDict['total']=0
for l in orderedLanguages:
    countDict[l]=0


##for l in L:
##    try:
##        curCount = lineCount(l+"-wikipedia.csv")
##        countDict[l]=curCount
##        countDict["total"]+=curCount
##    except IOError:
##        countDict[l]=0

fname = 'all-wikipedia.csv'
f= open(fname,'r')
fnameOut = 'all-wikipedia-normalized.csv'
fOut = open(fnameOut,'wb')
for line in f:
    els = line.split(',')
    curLan = els[0]
    if curLan in orderedLanguages:
        countDict['total']+=1
        try:
            countDict[curLan]+=1
        except:
            countDict[curLan]=1
        if countDict[curLan] <= countTargets[curLan]:
            fOut.write(line)
f.close()
fOut.close()


        
output=open('counts.csv','wb')
output.write("language,count\n")
output.write('total,'+str(countDict['total'])+'\n')
for l in L:
    output.write(l+','+str(countDict[l])+'\n')
output.close()

