'''
Copyright Suhas Satish
Texata Finals 2015

References - sklearn, gensim library documentation page examples, blog posts from google searches
'''

import nltk
from urllib import urlopen
from bs4 import BeautifulSoup
from readability import Document
from nltk.stem.snowball import SnowballStemmer
from nltk.tag.stanford import StanfordNERTagger
from nltk.corpus import reuters
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import *
import datetime, re, sys
from sklearn.feature_extraction.text import TfidfVectorizer
from random import randint
import math
from __future__ import division
import gensim
from gensim import corpora, models, similarities

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

#twenty = fetch_20newsgroups()

def extract_entities(text):
  entities = []
  for sentence in nltk.sent_tokenize(text):
    chunks = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
    entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])
  return entities

#-----------------------------------------------------
cisco_xml = LazyCorpusLoader(
    'cisco_xml', XMLCorpusReader, r'(?!\.).*\.xml')

def tokenize_and_stem(text):
    tokens_inner = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    stemmer = SnowballStemmer("english")
    stemmed_tokens = [stemmer.stem(t) for t in tokens_inner]
    stemmed_tokens_no_stop = [stemmer.stem(t) for t in stemmed_tokens if t not in nltk.corpus.stopwords.words('english')]
    fdist2 = nltk.FreqDist(stemmed_tokens_no_stop)
    filtered_tokens = []

    # filter out any tokens not containing letters,numbers,- (e.g., numeric tokens, raw punctuation)
    for token in tokens_inner:
        if re.search('[a-zA-Z0-9\-\\\/]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

#this is the main entry point for code
def summarize_cisco_support_forum_texts():
    #cisco_plain_text = LazyCorpusLoader(
    #    'content', PlaintextCorpusReader, r'(?!\.).*\.txt', encoding='latin_1')
    cisco_plain_text = LazyCorpusLoader(
        'cisco_forum_subset', PlaintextCorpusReader, r'(?!\.).*\.txt', encoding='latin_1')
    token_dict = {}
    for article in cisco_plain_text.fileids():
        token_dict[article] = cisco_plain_text.raw(article)

    tfidf = TfidfVectorizer(tokenizer=tokenize_and_stem, stop_words='english', decode_error='ignore')

    sys.stdout.flush()

    #creates Compressed Sparse Row format numpy matrix
    tdm = tfidf.fit_transform(token_dict.values())
    feature_names = tfidf.get_feature_names()

    #problem_statement_#1 - summarize support_forum articles automatically
    for article_id in range(0,tdm.shape[0] - 2):
        article_text = cisco_plain_text.raw(cisco_plain_text.fileids()[article_id])
        sent_scores = []
        for sentence in nltk.sent_tokenize(article_text):
            score = 0
            sent_tokens = tokenize_and_stem(sentence)
            for token in (t for t in sent_tokens if t in feature_names):
                score += tdm[article_id, feature_names.index(token)]
            sent_scores.append((score / len(sent_tokens), sentence))
        summary_length = int(math.ceil(len(sent_scores) / 5))
        sent_scores.sort(key=lambda sent: sent[0])
        print '\n*** SUMMARY ***'
        for summary_sentence in sent_scores[:summary_length]:
            print summary_sentence[1]
        print '\n*** ORIGINAL ***'
        print article_text

    #problem_statement_#2 - automatically categorize forum posts by tags into various groups
    reduce_dimensionality_and_cluster_docs(tfidf,tdm,num_features=200)

    #problem_statement_#3 - find similar documents to a current document (that user is reading) automatically
    #eg - quora: find similar questions, find similar answers
    cosine_similarity(tdm[0:1], tdm)
    '''
    output looks like this
    array([[ 1.        ,  0.22185251,  0.0215558 ,  0.03805012,  0.04796646,
         0.05069365,  0.05507056,  0.03374501,  0.03643342,  0.05308392,
         0.06002623,  0.0298806 ,  0.04177088,  0.0844478 ,  0.07951179,
         0.02822186,  0.03036787,  0.11022385,  0.0535391 ,  0.10009412,
         0.07432719,  0.03753424,  0.06596462,  0.01256566,  0.02135591,
         0.13931643,  0.03062681,  0.02595649,  0.04897851,  0.06276997,
         0.03173952,  0.01822134,  0.04043555,  0.06629454,  0.05436211,
         0.0549144 ,  0.04400169,  0.05157118,  0.05409632,  0.09541703,
         0.02473209,  0.05646599,  0.05728387,  0.04672681,  0.04519217,
         0.04126276,  0.06289187,  0.03116767,  0.04828476,  0.04745193,
         0.01404426,  0.04201325,  0.023492  ,  0.07138136,  0.03778315,
         0.03677206,  0.02553581]])
    The first document is compared to the rest, with the most similar to it being itself with score of 1, next most similar to it is document with score 0.22185251
    '''

    cosine_similarities = linear_kernel(tdm[0:1], tdm).flatten()

    #mapping back to document_name space
    related_docs_indices = cosine_similarities.argsort()
    '''
    document_ids
    array([23, 50, 31, 24,  2, 52, 40, 56, 27, 15, 11, 16, 26, 47, 30,  7,  8,
       55, 21, 54,  3, 32, 45, 12, 51, 36, 44, 43, 49,  4, 48, 28,  5, 37,
        9, 18, 38, 34, 35,  6, 41, 42, 10, 29, 46, 22, 33, 53, 20, 14, 13,
       39, 19, 17, 25,  1,  0])

       docs 0 and 1 are very similar which are the following posts (last 2 array elements above when sorted)
        https://supportforums.cisco.com/discussion/11469881/aniserver-failed-run-lms-40
        and
        supportforums.cisco.com/discussion/11469606/eos-lms-31-support-quest
    '''

    cosine_similarities[related_docs_indices]
    for key, value in token_dict.iteritems():
        print key, value
    #find the actual posts which are the most similar
    tfidf.inverse_transform(tdm)[0]
    tfidf.inverse_transform(tdm)[1]

def reduce_dimensionality_and_cluster_docs(tfidf,term_document_numpy_sparse_matrix,num_features):
    print("Performing dimensionality reduction using LSA")
    #n_components = num_features = 200
    svd = TruncatedSVD(num_features)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)
    X = lsa.fit_transform(term_document_numpy_sparse_matrix)
    #explained_variance = svd.explained_variance_ratio_.sum()
    #print("Explained variance of the SVD step: {}%".format(
    #    int(explained_variance * 100)))
    km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=3)
    km.fit(X)
    print km.labels_
    '''
    output looks like this
    array([3, 3, 4, 2, 2, 3, 4, 4, 2, 0, 3, 0, 3, 0, 3, 0, 4, 4, 0, 3, 2, 3, 3,
       4, 1, 0, 1, 1, 2, 2, 1, 1, 2, 2, 4, 4, 2, 1, 2, 4, 2, 0, 4, 2, 1, 2,
       3, 4, 0, 4, 2, 4, 4, 3, 2, 4, 0], dtype=int32)
    '''

    '''
     human readable format of clusters above
    '''
    print("Top terms per cluster:")
    original_space_centroids = svd.inverse_transform(km.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]

    terms = tfidf.get_feature_names()
    for i in range(5):
        print("Cluster %d:" % i)
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind])
        print()



def find_item_similarity_using_gensim(tdm):
    #find item similarity
    corpus = gensim.matutils.Sparse2Corpus(tdm,documents_columns=False)
    gensim_tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(gensim_tfidf[corpus], num_features=3494)
    vec = [(0, 1), (4, 1)]
    sims = index[gensim_tfidf[vec]]
    print(list(enumerate(sims)))
    #lsi = models.LsiModel(cisco_plain_text, num_topics=200)
    #dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
    #corpus = corpora.MmCorpus('/tmp/deerwester.mm')

def get_bag_of_words_model_for_gensim():
    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # remove words that appear only once
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    from pprint import pprint   # pretty-printer
    pprint(texts)





'''

'''