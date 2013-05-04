import string
#import readline
import csv
#f = csv.reader(open("data/wikipedia_all.csv", "rU"), dialect=csv.excel_tab)
#languages = ['en','de','fr','nl','it','ru','es','pl','sv','ja','zh','vi']

languages = ['en', 'de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs']
languageNames = {'en':'English', 'de':'German', 'pt':'Portuguese','fr':'French', 'nl':'Dutch', 'it':'Italian', 'ru':'Russian', 'es':'Spanish', 'pl':'Polish', 'sv':'Swedish', 'ja':'Japanese','zh':'Chinese','vi':'Vietnamese', 'uk':'Ukranian', 'ca':'Catalan', 'no':'Norwegian', 'ceb':'Cebuano', 'fi':'Finnish', 'war':'Waray-Waray', 'cs':'Czech'}
languageCoefficients = {'en':1, 'de':.202323, 'nl':.061875, 'pt':.05977438, 'fr':.104025, 'it':.104025, 'ru':.102992, 'es':.117026, 'sv':.03679, 'pl':.060417, 'ja':.079548, 'vi':.018557, 'zh':.044743, 'uk':0.0211179, 'ca':0.0197045262, 'no':0.02129933371, 'ceb':0.00428265275, 'fi':0.02284224547, 'war':0.00471009937, 'cs':0.01730745545}

data1 = open('data1.csv','w')
data2 = open('data2.csv', 'w')
#languageTimes = {'en':{},'de':{},'fr':{},'nl':{},'it':{},'ru':{},'es':{},'pl':{},'sv':{},'ja':{}}
languageTimes = {}
for language in languages:
	print language
	f = csv.reader(open("data/"+language+"-wikipedia.csv", "rU"), dialect=csv.excel_tab)
	totalEdits = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, '11':0, '12':0, '13':0, '14':0, '15':0, '16':0, '17':0, '18':0, '19':0, '20':0, '21':0, '22':0, '23':0, 'total':0}
	for record in f:
		#Each record in a single .csv document
		#record[0] = language code
		#record[1] = time edit was made
		recordTime = ""
		if len(record) != 0:
			record = string.split(record[0], ',')
			#row is not corrupted
			if len(record) > 8:
				recordTime = string.split(record[1], ':')
			if record[0] == language and len(recordTime) == 2:
				#Trims any leading zeros
				if len(recordTime[0]) == 2 and recordTime[0][0] == '0':
					recordTime[0] = recordTime[0][1:]
				#adds one to the total edits thing in the appropriate place
				totalEdits[recordTime[0]] = totalEdits[recordTime[0]] + 1
				totalEdits['total'] = totalEdits['total'] + 1
	print totalEdits
	print "Total dits are: "+str(totalEdits['total'])
	languageTimes[language]= totalEdits
	#After all the records are tallied up, put them in the "languageTime" Dict
print languageTimes
languageString = "time"
for language in languages:
	languageString += ","+language
data1.write(languageString+"\n")
data2.write(languageString+"\n")
for i in range(0, 24):
	timeString1 = str(i)
	timeString2 = str(i)
	#timeString += '+'+str(float(int((float(languageTimes['nl'][str(i)])/float(languageTimes['nl']['total']))*10000))/100.0)
	for language in languages:
		print "language is: "+language;
		print "language times is: "
		print languageTimes[language]
		timeString1 += ','+str(float(int((float(languageTimes[language][str(i)])/float(languageTimes[language]['total']))*10000))/100.0)
		timeString2 += ','+str(float(int(languageCoefficients[language]*(float(languageTimes[language][str(i)])/float(languageTimes[language]['total']))*10000))/100.0)
	data1.write(timeString1+"\n");
	data2.write(timeString2+"\n");
