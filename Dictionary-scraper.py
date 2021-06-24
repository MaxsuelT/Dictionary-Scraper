from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, Tag

"""
    Loading the page
"""
def getWord(word):
    try:    
        req = Request('https://www.ldoceonline.com/dictionary/'+ word)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36')
        html = urlopen(req)    
    except HTTPError as e:
        print(e.code)
        print(e.read())
    except URLError as error:
        print(error)
        print(error)
    
    soupObj = BeautifulSoup(html, 'html.parser')  
    pageFound = soupObj.find('link', rel='canonical')
    if pageFound['href'] != req.get_full_url():
        raise Exception('Page does not exist')
    return soupObj

"""
    Initial set up
"""
# Type the word you are looking for here
soup = getWord('hello')

body = soup.find('body')
DictEntry = body.find_all('span', class_='dictentry')

def findTag(obj, tag, cl, lmt=None):
    if lmt:
        try:
            return obj.find_all(tag, class_=cl, limit=lmt)
        except AttributeError as e:
            print(e)
    else:
        try:
            return obj.find(tag, class_=cl)
        except AttributeError as e:
            print(e)

def getDict(obj, name):
    output = {}
    for idx, val in enumerate(obj):
        output[name + str(idx + 1)] = val
    return output


unwantedTags = ['script', 'noscript', 'img', 'header']
unwantedClasses = ['header', 'responsive_cell2','topslot-container','footer', 'etym']
unwantedDivs = ["ad_leftslot_container"]
def decompose_(tag, cssClass, ids):
    if tag:
        [tg.decompose() for tg in body.find_all(tag)]
    if cssClass:
        [cl.decompose() for cl in body.find_all(class_=cssClass)]
    if ids:
        [cl.decompose() for cl in body.find_all(id=ids)]


decompose_(unwantedTags, unwantedClasses, unwantedDivs)

"""
    Title, Pronounciation
"""
title = body.find('h1', 'pagetitle').get_text()
pron = body.find('span','PRON').get_text() 
print('Definition of the word: ', title.title())
print('\nPronounciation: ', pron)


"""
    Audio 
"""

def getAudio(obj, name, tag, cl, lmt):
    result = []
    for exp in obj:
        ResultSet = findTag(exp,tag,cl, lmt)
        for elem in ResultSet:
            result.append(elem.get('data-src-mp3', -1))
            output = getDict(result, name)
    
    return output

audioBre = 'speaker brefile fas fa-volume-up hideOnAmp'
audioAme = 'speaker amefile fas fa-volume-up hideOnAmp'

pronLinks = getAudio(DictEntry, 
                    'Example ', 'span',{audioAme, audioBre}, 2)

print('\nPronounciation: ', pronLinks)

adExp = 'speaker exafile fas fa-volume-up hideOnAmp'
audioExamples = getAudio(DictEntry, 'Example', 'span', adExp, 2)
print('\nAudioExamples: ', audioExamples)

"""
     Grammar, Parts of speech
"""
def getGrPos(obj, name, tag, cl, lmt=None):
    result = []
    for elem in obj:
        strings = findTag(elem, tag, cl, lmt).get_text(strip=True)
        result.append(strings)
        output = getDict(result, name)
    return output

try:
    grm = getGrPos(DictEntry,'Grammar', 'span', 'GRAM')
    print('\nGrammar ', grm)
except AttributeError:
    pass

try:
    pos = getGrPos(DictEntry,'Pos', 'span', 'POS')
    print('\nParts of speech', pos)
except AttributeError:
    pass
"""
    Definition and examples
"""

def getExamples(obj,name, tag, cl, lmt=None):
    result = []
    for exp in obj:
        ResultSet = findTag(exp,tag,cl, lmt)
        for elem in ResultSet:
            result.append(elem.get_text())
            result = [string.strip() for string in result]
            output = getDict(result, name) 
    return output


try:
    defs = getExamples(DictEntry, 'Definition ',  'span', 'DEF', 2)
    print('\nDefinition: ', defs)
except AttributeError:
    pass 

try:
    exps = getExamples(DictEntry, 'Example ', 'span', 'EXAMPLE', 2)
    print('\nExamples: ', exps)
except AttributeError:
    pass 
