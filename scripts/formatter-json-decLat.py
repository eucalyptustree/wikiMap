filename = "all-wikipedia.csv"

#filename = "all-wikipedia-1000.csv"

languages20 = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs']

languages = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','fa','cs','hu','ko','ro','ar','tr','id','kk','ms','sr','sk','eo','da','lt','eu','bg','he','sl','hr','vo','et','hi','uz','gl','nn','simple','az','la','el','th','sh','ka','oc','new','mk','tl','pms','be','ht','ta','te','be-x-old','lv','br','mg','sq','hy','jv','cy','mr','lb','is','tt','bs','my','yo','ba','ml','an','lmo','af','fy','pnb','bn','sw','bpy','io','ky','ur','scn','ne','gu','zh-yue','nds','ku','ga','ast','qu','su','cv','sco','ia','als','bug','nap','bat-smg','map-bms','kn']
languages5 = languages[0:5]
languages10 = languages[0:10]
languages15 = languages[0:15]
f = open(filename,'r')

'''
Line contents:
0: lang
1: time
2: ip
3: lat
4: lon
5: city
6: country
7: article
'''


D = {}
hours = []
for i in range(24):
    hours.append(str(i))
for lan in languages:
    D[lan]= {}
    for h in hours:
        D[lan][h]={}
        D[lan][h]['countries']={}
        D[lan][h]['total']=0

D['all']={}
for h in hours:
    D['all'][h] = 0
i = 0


countries = []
IPs = []

for line in f:
    
    i+=1
    if i % 100000 == 0:
        print i
    #print line
    els = line.split(',')
    #good line = az	18:15	5.134.49.138	40.3953	49.8822	Baku	Azerbaijan	Da_Vin%C3%A7i_%C5%9Fifr%C9%99si_(kitab)
    if els[0] in languages and len(els[1].split(':')) == 2 and len(els[2].split('.')) == 4:
##        print els
##        raw_input()

        lan = els[0]
        time = els[1]
        hour = str(int(time.split(":")[0]))
        ip = els[2]
        IPs.append(ip)
        if lan in languages20:
            
            try:
                latInt, latDec = els[3].split('.')
                lat = str(latInt)+"."+str(latDec[0:1]) ## rounds lat to 1 decimal
            except ValueError:
                lat = els[3]
                #print "doublecheck... lat:", lat

            try:
                
                lonInt, lonDec = els[4].split('.')
                lon = str(lonInt)+"."+str(lonDec[0:1]) ## rounds lon to 1 decimal

            except ValueError:
                lon = els[4]
                #print "doublecheck... lat:", lon

            latlon = lat+','+lon
            
            country = els[6]
            countries.append(country)
            try:
                D[lan][hour][latlon] +=1
            except:
                D[lan][hour][latlon] =1
            try:
                D[lan][hour]['countries'][country] +=1
            except:
                D[lan][hour]['countries'][country] =1
            D[lan][hour]['total']+=1
            D['all'][hour]+=1


for lan in languages20:

        for h in hours:

            filename = lan+str(h)+'.json'
            output = open(filename,'w')
            output.write('{"type":"FeatureCollection","features":[')
            output.write('\n')
            curDict = D[lan][h]
            curTotal = D[lan][h]['total']
            for k in curDict.keys():
                #print lan+','+h+','+k
                if k == 'total':
                    pass
                elif k=='countries':
                    pass #output countries stats to diff file
                elif type(k) != 'dict':
                    
                    curLat , curLon = k.split(',')
                    try:
                        #print curLat, curLon
                        outLine = '{"type":"Feature","properties":{'
                        outLine+= '"edits":'+str(curDict[k])+'},"geometry":{"type":"Point","coordinates":['+curLon+','+curLat+']}}, '
                        #output ip : stats to file
                        #outLine = "{ \n    latitude: "+curLat+",\n    longitude: "+curLon+",\n    edits: "+str(curDict[k])+",\n    lan: '"+lan+"',\n    radius:0,\n    hour: "+str(h)+",\n},\n"
                        output.write(outLine)
                        
                        outLineInt = '{"type":"Feature","properties":{'
                        outLineInt+= '"edits":'+str(curDict[k])+'},"geometry":{"type":"Point","coordinates":['+str(int(float(curLon)))+','+str(int(float(curLat)))+']}}, '
                        
                        
                    except:
                        #print 'broke:',curLat, curLon
                        
                        pass
            output.write(']}')
            output.close()

