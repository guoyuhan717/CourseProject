import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import web_scraping
from web_scraping import *
import ner
from ner import *
import webbrowser

root = Tk()
root.title('Entity-Based Knowledge Application')
root.geometry("800x600")

def callback(url):
   webbrowser.open_new_tab(url)

label1 = Label(root, text="Please enter the url:")
label1.pack()
text = Text(root, width=100, height=10)
text.pack()

def get_output():
    url = text.get("1.0", "end-1c")
    print(url)
    print(type(url))
    result_news = []
    if (url != None):
        #create a webdriver object and set options for headless browsing
        options = Options()
        options.headless = True
        driver = webdriver.Chrome('./chromedriver',options=options)
        news = scrape_news_page(url,driver)
        driver.close()

        news = sent_tokenize(news)

        for x in news:
            result_news.append(word_tokenize(x))

        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        device = 'cuda'
        TRANSFORMERS_CACHE = os.path.join(os.getenv('TRANSFORMERS_CACHE'),
                                             "dslim/bert-base-NER") if 'TRANSFORMERS_CACHE' in os.environ else None

        docs = []
        docs.append(result_news)

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
        # print(len(entities))
        # print(entities)
        #
        # entikty linking
        entities = get_urls(entities)
        # print(len(entities))
        # print(entities)

        # entity extension
        entities = get_extensions(entities)
        #print(type(entities))
        keys = list(entities.keys())
        #print(len(entities))
        for i in range(10):
            print(entities[keys[i]]['url'])
    if len(result_news) > 0:
        label2.config(text='Here are 10 entities and their corresponding urls:')
        link1 = Label(root, text=entities[keys[0]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link1.pack()
        link1.bind("<Button-1>", lambda e: callback(entities[keys[0]]['url']))

        link2 = Label(root, text=entities[keys[1]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link2.pack()
        link2.bind("<Button-1>", lambda e: callback(entities[keys[1]]['url']))

        link3 = Label(root, text=entities[keys[2]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link3.pack()
        link3.bind("<Button-1>", lambda e: callback(entities[keys[2]]['url']))

        link4 = Label(root, text=entities[keys[3]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link4.pack()
        link4.bind("<Button-1>", lambda e: callback(entities[keys[3]]['url']))

        link5 = Label(root, text=entities[keys[4]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link5.pack()
        link5.bind("<Button-1>", lambda e: callback(entities[keys[4]]['url']))

        link6 = Label(root, text=entities[keys[5]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link6.pack()
        link6.bind("<Button-1>", lambda e: callback(entities[keys[5]]['url']))

        link7 = Label(root, text=entities[keys[6]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link7.pack()
        link7.bind("<Button-1>", lambda e: callback(entities[keys[6]]['url']))

        link8 = Label(root, text=entities[keys[7]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link8.pack()
        link8.bind("<Button-1>", lambda e: callback(entities[keys[7]]['url']))

        link9 = Label(root, text=entities[keys[8]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link9.pack()
        link9.bind("<Button-1>", lambda e: callback(entities[keys[8]]['url']))

        link10 = Label(root, text=entities[keys[9]]['url'],font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link10.pack()
        link10.bind("<Button-1>", lambda e: callback(entities[keys[9]]['url']))

button = Button(root, text="Submit", command=get_output)
button.pack()

label2 = Label(root, text="", font=('Calibri 15'))
label2.pack()

root.mainloop()
