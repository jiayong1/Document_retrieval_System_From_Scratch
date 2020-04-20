import gensim 
from gensim.models import Word2Vec 
from nltk.tokenize import word_tokenize, sent_tokenize 
all_text = open("all_text.txt", "r") 
f = all_text.read().replace("\n", " ") 
data = [] 
for i in sent_tokenize(f): 
    temp_list = []
    for j in word_tokenize(i): 
        if j.lower().isalpha():
            temp_list.append(j.lower()) 
    data.append(temp_list) 

w2v_model = gensim.models.Word2Vec(data, min_count = 10,size = 500, window = 15, sg = 1)
w2v_model.save("WordEmbedding.model")