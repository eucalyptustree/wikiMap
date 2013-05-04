orderedLanguages = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','fa','cs','hu','ko','ro','ar','tr','id','kk','ms','sr','sk','eo','da','lt','eu','bg','he','sl','hr','vo','et','hi','uz','gl','nn','simple','az','la','el','th','sh','ka','oc','new','mk','tl','pms','be','ht','ta','te','be-x-old','lv','br','mg','sq','hy','jv','cy','mr','lb','is','tt','bs','my','yo','ba','ml','an','lmo','af','fy','pnb','bn','sw','bpy','io','ky','ur','scn','ne','gu','zh-yue','nds','ku','ga','ast','qu','su','cv','sco','ia','als','bug','nap','bat-smg','map-bms','kn']
def getNum():
    numDir = raw_input("How many directories are you combining?\n... ")
    try:
        numDir = int(numDir)
        return numDir
    except ValueError:
        print "Please enter an integer value."
        getNum()
        
numDirs = getNum()   
dirs = []
for i in range(numDirs):
    dirs.append(str(i+1))

#print dirs

for d in dirs:
    #print d
    for lang in orderedLanguages:
        try:
            curFile = open("./"+d+'/'+lang+"-wikipedia.csv", 'rb')
            #print "file: "+d+"//"+lang+" exists"
            if not curFile.closed:
                #print d,lang
                #print "dir: "+d", file:"+ang+" exists"
                try:
                    output = open("./merged/"+lang+"-wikipedia.csv", 'ab')
                    #print "opened file for append"
                except IOError:
                    output = open("./merged/"+lang+"-wikipedia.csv", 'wb')
                    #print "opened file for write"
                try:
                    output2 = open("./merged/"+"all-wikipedia.csv", 'ab')
                except IOError:
                    output2 = open("./merged/"+"all-wikipedia.csv", 'wb')
                for line in curFile:
                #print line
                    output.write(line)
                    output2.write(line)
            output.close()
            output2.close()
            curFile.close()    
        except IOError:
            #print "error"
            pass
##            input = open(lang+"-wikipedia.csv", 'wb')
##            for line in input:
##                print line
##                output.write(line)
##                output2.write(line)
