from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = 'cuda'
TRANSFORMERS_CACHE = os.path.join(os.getenv('TRANSFORMERS_CACHE'),
                                     "dslim/bert-base-NER") if 'TRANSFORMERS_CACHE' in os.environ else None


def ner_sent(nlp, sent):
    # https://huggingface.co/dslim/bert-base-NER
    # example = "My name is Wolfgang and I live in Berlin"
    ner_results = nlp(sent)
    # print(sent)
    # print(ner_results)
    return ner_results



def read_file(file_name):
    docs = []
    with open(file_name,'r') as f:
        lines = f.readlines()
        for line in lines:
            sentences = line.replace('\',\'','').replace('\'','').split('], [')
            docs.append([sent.replace('[','').replace(']','').split(',') for sent in sentences])

    # print(len(docs))
    # print(len(docs[0]))
    return docs

def get_urls(entities):
    res = dict()
    for ent in entities:
        url = 'https://en.wikipedia.org/wiki/'+ ent
        r = filter_invalid_url(url)
        if r is not None:
            res[ent]=r
    return res

def filter_invalid_url(url):
    response = requests.get(url)
    if 'Main_Page' not in response.url:

        soup=BeautifulSoup(response.text,'lxml')
        data=soup.select('#noarticletext > tbody > tr > td > b')
        if len(data) == 0:
            return {'url':response.url,'soup':soup}
    return None

def extend_entities(soup):
    res = []
    # first paragraph
    # fp = soup.select('#mw-content-text > div.mw-parser-output > p:nth-child(8)')
    for item in soup.find_all('a'):
        try:
            h = item.get('href')
            if not (h.startswith('#') or 'File' in h):
                res.append('https://en.wikipedia.org'+h)
        except:
            continue

    return res[:10]

def get_extensions(entities):
    res = dict()
    for ent in entities:
        elist = extend_entities(entities[ent]['soup'])
        if len(elist) > 0:
            res[ent] = {'url':entities[ent]['url'], 'extend':elist}
    return res

if __name__ == "__main__":

    docs = read_file('news_1(1).txt')

    # NER: extract entities
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER", cache_dir=TRANSFORMERS_CACHE)
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER", cache_dir=TRANSFORMERS_CACHE)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)


    entities = set()
    for doc in docs:
        for sent in doc:
            s = ' '.join(sent)
            ner_res = ner_sent(nlp,s)
            entities.update([e['word'] for e in ner_res])
    print(len(entities))
    print(entities)

    # entikty linking
    entities = get_urls(entities)
    print(len(entities))
    print(entities)

    # entity extension
    entities = get_extensions(entities)
    print(len(entities))
    print(entities)