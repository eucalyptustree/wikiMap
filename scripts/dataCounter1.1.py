
##def lineCount(fname):
##    count = 0
##    f = open(fname, 'rb')
##    for l in f:
##        count+=1
##    #print count
##    return count
        
orderedLanguages = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','fa','cs','hu','ko','ro','ar','tr','id','kk','ms','sr','sk','eo','da','lt','eu','bg','he','sl','hr','vo','et','hi','uz','gl','nn','simple','az','la','el','th','sh','ka','oc','new','mk','tl','pms','be','ht','ta','te','be-x-old','lv','br','mg','sq','hy','jv','cy','mr','lb','is','tt','bs','my','yo','ba','ml','an','lmo','af','fy','pnb','bn','sw','bpy','io','ky','ur','scn','ne','gu','zh-yue','nds','ku','ga','ast','qu','su','cv','sco','ia','als','bug','nap','bat-smg','map-bms','kn']


countDict={}
L = orderedLanguages
countDict['total']=0
for l in L:
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
for line in f:
    els = line.split(',')
    curLan = els[0]
    if curLan in orderedLanguages:
        countDict['total']+=1
        try:
            countDict[curLan]+=1
        except:
            countDict[curLan]=1

            
        
output=open('counts.csv','wb')
output.write("language,count\n")
output.write('total,'+str(countDict['total'])+'\n')
for l in L:
    output.write(l+','+str(countDict[l])+'\n')
output.close()

