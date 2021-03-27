# -*- coding: utf-8 -*-
"""Homeowork5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OzfI4sxZUTTYHIdWuI_CoYVlPlw0Bncw
"""

!pip install spacy
!pip install newsapi-python 
!pip install en_core_web_lg
#import en_core_web_lg
import string
import nltk

from wordcloud import WordCloud 
from nltk import pos_tag
nltk.download('stopwords')
from newsapi import NewsApiClient
from collections import Counter
import matplotlib.pyplot as plt

import spacy
!python -m spacy download en_core_web_lg
nlp_eng = en_core_web_lg.load()
#nlp_eng = spacy.load('en_core_web_lg')
newsapi = NewsApiClient (api_key='406ab481da43405bae670eda5c5a588e')



articles = []
for i in range(1,6):
  temp = articles.append(newsapi.get_everything(q='coronavirus', language='en', from_param='2021-02-26', to='2021-03-25', sort_by='relevancy', page=i))
import pickle
filename = 'articlesCOVID.pckl'
pickle.dump(articles, open(filename, 'wb'))
filename = 'articlesCOVID.pckl'
loaded_model = pickle.load(open(filename, 'rb'))
filepath = '/content/articlesCOVID.pckl'
pickle.dump(loaded_model, open(filepath, 'wb'))

import pandas as pd
dados = []

for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        description = x['description']
        date = x['publishedAt']
        content = x['content']
        
        dados.append({'title':title, 'date':date, 'desc':description, 'content':content})
print(dados)
df = pd.DataFrame(dados)
df = df.dropna()
df.head()

tokenizer = RegexpTokenizer(r'\w+')

def get_keywords_eng(token):
  result = []
  punctuation = string.punctuation
  stop_words = stopwords.words('english')
  
  for i in token:
    if (i in stop_words):
      #print(i)
      continue
    else:
      result.append(i)
  
  #if (token in nlp_eng.Defaults.stop_words or token in punctuation):
    #pass
  #if (token.pos_ in pos_tag):
    #result.append(token)
  return result

results = []
for content in df.content.values:
    #print(content)
    #content = content.split(" ")
    #for a in content:
    content = tokenizer.tokenize(content)
    #print(a)
    results.append([x[0] for x in Counter(get_keywords_eng(content)).most_common(5)])
df['keywords'] = results
print(results)

text = str(results)
print(text)
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()