from bs4 import BeautifulSoup
import urllib.request
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import urllib3


myProxyList = ['212.147.36.52:80', '23.108.80.194:53412', '23.108.80.227:13381', '23.108.80.132:30504',
               '23.108.80.245:54921', '23.108.80.64:32665', '23.108.80.47:43876', '23.108.80.68:56911',
               '23.108.80.53:22342', '23.108.80.122:29340']

class Entry:
        def __init__(self, entryNum, sentence):
            self.entryNum = entryNum
            self.sentence = sentence
            self.lenght = len(sentence)


        def __str__(self):
            return "Entry Num: %d, Sentence: %s" % (self.entryNum, self.sentence)

def get_inci_db():
    client = MongoClient('localhost', 27017)
    inciDb = client.inciDb
    return inciDb

def get_entry_collection():
    db = get_inci_db()
    collection = db.entry
    return collection

def get_processes_collection():
    db = get_inci_db()
    collection = db.processes
    return collection

def get_soup_object(url, n = 0):
    #http = urllib3.proxy_from_url('http://' + myProxyList[int(n)])
    html = urllib.request.urlopen(url).read()
    r = html.decode("utf8")
    soup = BeautifulSoup(r, 'html.parser')
    return soup

def is_sentence_valid(sentence):
    temp = sentence.rstrip(' \t\n\r')
    temp = temp.lstrip(' \t\n\r')
    return not (len(temp)<32 or temp.__contains__('http://') or temp.startswith('--spoiler--'))
