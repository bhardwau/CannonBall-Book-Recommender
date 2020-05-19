#!/usr/bin/env python
# coding: utf-8

# In[164]:


import pandas as pd
import sklearn
import re
import nltk
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import string
from gensim import corpora
from gensim.models import LsiModel
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.coherencemodel import CoherenceModel
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[165]:


book_data = pd.read_csv("books.csv")
user_data = pd.read_csv("users.csv")


# In[168]:


book_data.keys()


# In[169]:


book_data = book_data.drop(['publication_day','isbn','isbn13','publication_month','publication_day','is_ebook','work','average_rating','num_pages','format','edition_information','ratings_count','book_links','series_works','similar_books'],axis = 1)


# In[171]:


book_data = book_data.drop(['asin','kindle_asin','marketplace_id','country_code','text_reviews_count','public_document'], axis = 1)


# In[172]:


book_data.keys()


# In[173]:


book_data = book_data.drop(['_id','id'], axis = 1)


# In[177]:


book_data.head()


# In[178]:


for i in range (book_data.shape[0]):
        book_data.iloc[i,6] = re.sub(r"[^a-zA-Z]+", ' ', book_data.iloc[i,6])


# In[179]:


word = ['name','count','shelf']
for i in range(book_data.shape[0]):
    word_list = book_data.iloc[i,6].split();
    book_data.iloc[i,6] = ' '.join([i for i in word_list if i not in word])


# In[180]:


for i in range (book_data.shape[0]):
        book_data.iloc[i,5] = re.sub(r"[^a-zA-Z]+", ' ', book_data.iloc[i,5])


# In[181]:


word = ['name','count','shelf']
for i in range(book_data.shape[0]):
    word_list = book_data.iloc[i,6].split();
    book_data.iloc[i,6] = ' '.join([i for i in word_list if i not in word])


# In[184]:


def pre_process(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", " ")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", " "))
        else:
            return ''


# In[185]:


columns = ['description','authors','publisher','popular_shelves']

for f in columns:
    book_data[f] = book_data[f].apply(pre_process)


# In[186]:


def combine(x):
    return  (x['description']) + ' ' + (x['authors']) + ' ' + (x['publisher']) + ' ' + (x['popular_shelves'])


# In[188]:


book_data['train'] = book_data.apply(combine,axis = 1)


# In[190]:


word_stopped = TfidfVectorizer(stop_words='english')

book_data['train'] = book_data['train'].fillna('')

matrix = word_stopped.fit_transform(book_data['train'])


# In[192]:


co_sim = linear_kernel(matrix,matrix)


# In[194]:


book_data = book_data.reset_index()


# In[195]:


indexing = pd.Series(book_data.index, index=book_data['title']).drop_duplicates()


# In[ ]:


indexing = pd.Series(book_data.index, index=book_data['title','publisher']).drop_duplicates()


# In[223]:


resultss = []


# In[228]:


def get_recommendations(title,cosine_sim1 = co_sim):
    index = indexing[title]
    similarity = list(enumerate(cosine_sim1[index]))
    
    similarity = sorted(similarity,key=lambda i: i[1], reverse = True)
    
    similarity = similarity[1:20]
    
    movie_index = [j[0] for j in similarity ]
    resultss = book_data['title'].iloc[movie_index]
    return resultss


# In[229]:


book_data['title'][323]


# In[230]:


get_recommendations('The Door Into Summer')


# In[126]:


get_recommendations("Darwin's Dangerous Idea: Evolution and the Meanings of Life")


# In[162]:


get_recommendations("Darwin's Dangerous Idea: Evolution and the Meanings of Life")


# In[200]:


get_recommendations("Darwin's Dangerous Idea: Evolution and the Meanings of Life")


# In[203]:


get_recommendations('Storage Area Network Essentials: A Complete Guide to Understanding and Implementing Sans')


# In[208]:


get_recommendations('Letterhead and Logo Design 9')


# In[213]:


get_recommendations('What to Expect the First Year (What to Expect)')


# In[217]:


get_recommendations('The Fellowship of the Ring (The Lord of the Rings, #1)')


# In[227]:


get_recommendations('eBay for Dummies')


# In[ ]:




