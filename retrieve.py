import re
import string
import pandas as pd
import utils
import pickle
import math
from collections import Counter
import argparse
import os
import nltk 
from nltk.corpus import stopwords 
from nltk.corpus import wordnet 
import gensim 
from gensim.models import Word2Vec 
from googletrans import Translator
from nltk import tokenize
translator = Translator()


def dictionary_expansion(query_words_list, query_words_pos):

    query_words_list = query_words_list*4
    word_to_add = set()
    for i in query_words_pos:
        word= i[0]
        syn = wordnet.synsets(word)
        if i[1][0] == "N":
            p = ["n"]
        elif i[1][0] == "V":
            p = ["v"]
        elif i[1][0] =="J":
            p = ["a", "s"]
        elif i[1][0:2] == "RB":
            p = ["r"]
        else:
            p = []

        for j in syn:
            if j.pos() in p:
                word_to_add.add(j.name().split('.')[0])
    word_to_add = list(word_to_add)
    for idx, val in enumerate(list(word_to_add)):
        if val in past_tense_and_plural:
            val = past_tense_and_plural[val]
        word_to_add[idx] = utils.porter_stemmer(val)
        if word_to_add[idx] not in query_words_list:
            query_words_list.append(word_to_add[idx])
            
    return query_words_list

def Word_Embedding_Expansion(query_words_list):
    word2model = gensim.models.Word2Vec.load("WordEmbedding.model")
    word_to_add = set()
    for i in query_words_list:
        if i in word2model.wv.vocab:
            word_to_add.add(word2model.wv.most_similar(positive = i, topn = 1)[0][0])
    word_to_add = list(word_to_add)
    for idx, val in enumerate(word_to_add):
        if val in past_tense_and_plural:
            val = past_tense_and_plural[val]
        word_to_add[idx] = utils.porter_stemmer(val)
    return word_to_add

def query(query_words_list, index_length):
    Query_tf = Counter(query_words_list)
    weight_tfidf = {}
    doc_length = 0
    for i in Query_tf:
        weight_tfidf[i] = (1+math.log10(Query_tf[i])) * math.log10(Document_Length/index_length[i])
        doc_length += weight_tfidf[i] ** 2
    doc_length = math.sqrt(doc_length)
    weight_tfidf = {k: v / doc_length for k, v in weight_tfidf.items()}
    return weight_tfidf

def document(query_words_list, Document_list, Score_df, tfidf_score,index_length,text_df):
    Query_tf = Counter(query_words_list)
    for doc in Document_list:
        text = text_df[int(doc)]
        document_tf_weight = {}
        doc_length = 1
        for i in Query_tf:
            count = text.count(i)
            if count>0:
                document_tf_weight[i] = (1+math.log10(count)) * math.log10(Document_Length/index_length[i])
            else:
                document_tf_weight[i] = 0
            doc_length += document_tf_weight[i] ** 2
        #print(doc_length)
        doc_length = math.sqrt(doc_length)
        document_tf_weight = {k: v / doc_length for k, v in document_tf_weight.items()}
        Score = 0
        for i in tfidf_score:
            Score_df.loc[Score_df.iloc[:,0] == int(doc), "Score"] += tfidf_score[i] * document_tf_weight[i]
        
    return Score_df







my_parser = argparse.ArgumentParser(description='retrieve info')
my_parser.add_argument('-l',action='store_true',help='linguistic-based/dictionary')
my_parser.add_argument('-e',action='store_true',help='embeddings-based')
my_parser.add_argument('-i',metavar='index-directory',type=str,help='the input index directory')
my_parser.add_argument('-q',metavar='query words',type=str,help='the query words')
my_parser.add_argument('-x',action='store_true',help='if you query is spanish')
my_parser.add_argument('-s',action='store_true',help='Only show the results for top 10 documents with snippet')


args = my_parser.parse_args()

stop_words = set(stopwords.words('english')) 
data = pd.read_csv("Full-Economic-News-DFE-839861.csv", encoding = "ISO-8859-1")
Document_Length = data.shape[0]

index_directory = args.i
query_words = args.q
linguistic_based = args.l
embeddings_based = args.e
spanish = args.x
snippet = args.s


if spanish:
    query_words = translator.translate(query_words,  dest='en').text


past_tense_and_plural = dict()
with open("past_tense_and_plural.txt") as f:
    for line in f:
        forms = line.split(",")
        base_form = forms[0]
        for j in range(1, len(forms)):
            past_tense_and_plural[forms[j].strip("\n")] = base_form


with open(index_directory+"Posting_List_Length.pkl", 'rb') as f:
    index_length = pickle.load(f)
with open(index_directory+"Posting_List.pkl", 'rb') as f:
    index = pickle.load(f)
with open(index_directory+"ID_and_Text.pkl", 'rb') as f:
    text_df = pickle.load(f)


query_words_list = re.sub(r'[^\w\s]','',query_words).lower().strip().split(" ")
if embeddings_based:
    Word_Embedding_Expansion_toadd = Word_Embedding_Expansion(query_words_list)


query_words_pos = nltk.pos_tag(query_words_list)

for idx, val in enumerate(query_words_list):
    if val in past_tense_and_plural:
        val = past_tense_and_plural[val]
    query_words_list[idx] = utils.porter_stemmer(val)

if linguistic_based:
    query_words_list = dictionary_expansion(query_words_list, query_words_pos)


if embeddings_based:
    query_words_list.extend(Word_Embedding_Expansion_toadd)


Document_list = set()
for i in query_words_list:
    if i in index.keys():
        Document_list.update(index[i])



query_words_list = [w for w in query_words_list if not w in stop_words and w in index.keys() ] 
print(query_words_list)

Score_df = pd.DataFrame(list(Document_list), columns = ['unit_id'])
Score_df["Score"] = 0
query_normalized_tfidf =  query(query_words_list, index_length)
Score_df = document(query_words_list, Document_list, Score_df, query_normalized_tfidf, index_length,text_df)


Score_df = Score_df.sort_values('Score',ascending = False ).reset_index(drop = True)

if not args.s:
    for index, row in Score_df.head(100).iterrows():
        print(index+1, str(int(row['unit_id']))+": ", "{0:.7f}".format(row["Score"]))

else:
    document_to_check = list(Score_df["unit_id"][0:10])
    for index, d in enumerate(document_to_check):
        sub_text = tokenize.sent_tokenize(data.loc[(data["_unit_id"] == d),"text"].item().replace("</br></br>"," "))
        text = sub_text.copy()
        for j in range(len(text)):
            sen_words_list = re.sub(r'[^\w\s]','',text[j]).lower().strip().split(" ")
            for i,v in enumerate(sen_words_list):
                if v in past_tense_and_plural:
                    v = past_tense_and_plural[v]
                sen_words_list[i] = utils.porter_stemmer(v)
            text[j] = " ".join(sen_words_list)
        
        Score_df_sentence = pd.DataFrame(list(range(len(text))), columns = ['sentence_id'])
        Score_df_sentence["Score"] = 0
        Score_df_sentence = document(query_words_list, list(range(len(text))), Score_df_sentence, query_normalized_tfidf, index_length, text )
        sentences_to_show = sorted(list(Score_df_sentence.sort_values("Score",ascending=False)["sentence_id"][0:3]))
        ret = ""
        for i in range(len(sentences_to_show)):
            if i == 0 and sentences_to_show[i] != 0:
                ret += " ... "
            elif i > 0 and sentences_to_show[i] != sentences_to_show[i-1] +1:
                ret += " ... "
            else:
                ret += " "
            ret += sub_text[sentences_to_show[i]]
        print(str(index)+"\t"+str(d)+"\t"+ret)






