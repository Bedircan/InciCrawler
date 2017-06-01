from HelperMethods import *
import sys
import threading

db = get_inci_db()
entryCollection = get_entry_collection()

#Getting the last processed entry number.
if entryCollection.count()>1:
    lastEntry = entryCollection.find_one(sort=[('entryNum', -1)])
    lastEntryNum = lastEntry['entryNum']
else:
    lastEntryNum = 100

print(lastEntryNum)

#This parameter is to define how many pages after the last one will be processed. It should be divisible to the Thread number.
howManyIteration = 10000

def create_entry_in_db(iterationNum, collection):
    mainUrl = "http://www.incisozluk.com.tr"
    url = "http://www.incisozluk.com.tr/e/" + str(iterationNum)
    soup = get_soup_object(url)
    try:
        link = soup.find('h1', {'class': 'title'}).find('a')
        createdLink = mainUrl + link['href']
        entryPage = get_soup_object(createdLink)
        temp = entryPage.find_all('div', {'class': 'entry-text-wrap'})
        for div in temp:
            if is_sentence_valid(div.text):
                entry = Entry(iterationNum, div.text)
                collection.insert_one(entry.__dict__)
                print(entry)
    except:
        temp = 0

def worker(first,last):

    for i in range(first+lastEntryNum,last+lastEntryNum):
        create_entry_in_db(i,entryCollection)
        print('Processing the entry %d, Worker num: %s' % (i,threading.currentThread().getName()))
    return

#It is to minimize duration roaming between pages.
howManyThread = 100

threads = []
for i in range(0,howManyThread):
    first = i*(howManyIteration/howManyThread)
    last = (i+1)*(howManyIteration/howManyThread)
    t = threading.Thread(target=worker, args=(int(first),int(last)))
    threads.append(t)
    t.start()

