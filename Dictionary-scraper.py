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
soup = getWord('amazing')

body = soup.find('body')
DictEntry = body.find_all('span', class_='dictentry')


unwantedTags = ['script', 'noscript', 'img']
unwantedClasses = ['header', 'responsive_cell2','topslot-container','footer', 'etym']
unwantedId = ["ad_leftslot_container"]


def decompose_(tag=None, cl=None, id_=None):
    [tg.decompose() for tg in body.find_all(tag, class_=cl, id=id_)]


decompose_(unwantedTags)
decompose_('div', unwantedClasses)
decompose_('div',None, unwantedId)

def getDict(obj, name):
    output = {}
    for idx, val in enumerate(obj):
        output[name + str(idx + 1)] = val
    return output

def getAudio(obj, name, tag, cl, lmt):
    result = []
    for audio in obj:
        resultSet = audio.find_all(tag, class_=cl, limit=lmt)
        for elem in resultSet:
            result.append(elem.get('data-src-mp3', -1))
            output = getDict(result, name)
    
    return output


def getGrPos(obj, name, tag, cl, lmt=None):
    result = []
    for elem in obj:
        strings = elem.find(tag, class_=cl).get_text(strip=True)
        result.append(strings)
        output = getDict(result, name)
    return output


def getExamples(obj,name, tag, cl, lmt=None):
    result = []
    for exp in obj:
        ResultSet = exp.find_all(tag, class_=cl, limit=lmt)
        for elem in ResultSet:
            result.append(elem.get_text())
            result = [string.strip() for string in result]
            output = getDict(result, name) 
    return output


"""
    Title, Pronounciation
"""

title = body.find('h1', class_='pagetitle').get_text()
pron = body.find('span',class_='PRON').get_text() 
print('Definition of the word: ', title.title())
print('\nPronounciation: ', pron)


"""
    Audio 
"""

AUDIOBRE = 'speaker brefile fas fa-volume-up hideOnAmp'
AUDIOAME = 'speaker amefile fas fa-volume-up hideOnAmp'
EXAMPLE = 'speaker exafile fas fa-volume-up hideOnAmp'

try:
    pronLinks = getAudio(DictEntry, 
                'Example ', 'span',{AUDIOAME, AUDIOBRE}, 2)
    print('\nPronounciation: ', pronLinks)
except AttributeError:
    pass

try: 
    audioExamples = getAudio(DictEntry, 'Example', 'span', EXAMPLE, 2)
    print('\nAudioExamples: ', audioExamples)
except AttributeError:
    pass

"""
     Grammar, Parts of speech
"""


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
