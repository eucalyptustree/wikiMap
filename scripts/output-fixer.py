
languages = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs','hu','ko','ro','ar','tr','id','kk','ms','sr','sk','eo','da','lt','eu','bg','he','sl','hr','vo','et','hi','uz','gl','nn','simple','az','la','el','th','sh','ka','oc','new','mk','tl','pms','be','ht','ta','te','be-x-old','lv','br','mg','sq','hy','jv','cy','mr','lb','is','tt','bs','my','yo','ba','ml','an','lmo','af','fy','pnb','bn','sw','bpy','io','ky','ur','scn','ne','gu','zh-yue','nds','ku','ga','ast','qu','su','cv','sco','ia','als','bug','nap','bat-smg','map-bms','kn']
languages5 = languages[0:5]
languages15 = languages[0:15]
languages20 = ['en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs']



hours = range(-1,0)

import fileinput
import sys

def replaceAll(f,searchExp,replaceExp):
    for line in fileinput.input(f, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

for lan in languages20:
    for h in hours:
        filename = lan+str(h)+'.json'
        replaceAll(filename, ']}}, ]}', ']}} ]}')


filename = 'all-all.json'
replaceAll(filename, ']}}, ]}', ']}} ]}')

