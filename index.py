import re
import string
import pandas as pd
import pickle
import utils
import argparse
import os

my_parser = argparse.ArgumentParser(description='Input and Output path')
my_parser.add_argument('-d',metavar='input_path',type=str,help='the input-file path')
my_parser.add_argument('-i',metavar='output_path',type=str,help='the output index directory')

args = my_parser.parse_args()

data = pd.read_csv(open(args.d, encoding = "utf8", errors ="ignore"))



data = data.sort_values('_unit_id')
past_tense_and_plural = dict()
with open("past_tense_and_plural.txt") as f:
    for line in f:
        forms = line.split(",")
        base_form = forms[0]
        for j in range(1, len(forms)):
            past_tense_and_plural[forms[j].strip("\n")] = base_form


Titles = "(Mr|Mrs|Ms|Dr|Inc|Ltd|Jr|Sr|Co)[.]"
def Word_Tokenization(i, unit_id ):
    tokens = set()
    i = i.replace("\n","")
    i = re.sub(Titles, "\\1<PERIODATHERE>", i)
    i = i.replace(". ", " ")
    i = i.replace("! ", " ")
    i = i.replace("? ", " ")
    i = i.replace(", ", " ")
    i = i.replace("<PERIODATHERE>", ".")    
    i = re.sub("([A-Za-z])[.]([A-Za-z])[.]([A-Za-z])[.]","\\1PERIODATHERE\\2PERIODATHERE\\3PERIODATHERE",i)
    i = re.sub("([A-Za-z])[.]([A-Za-z])[.]","\\1PERIODATHERE\\2PERIODATHERE",i)
    i = re.sub("([0-9])[.]([0-9])","\\1PERIODATHERE\\2",i)
    i = re.sub('([^\w\s^\'])', r' \1 ', i)
    i = re.sub('\s{2,}', ' ', i)
    i = i.replace("PERIODATHERE", ".")
    words = i.strip(string.punctuation).split(" ")
    for word in words:
        the_word = word
        if the_word in past_tense_and_plural:
                the_word = past_tense_and_plural[the_word]
        the_word = utils.porter_stemmer(the_word)
        if the_word not in string.punctuation:
            tokens.add(the_word)
    for i in tokens:
        if i not in all_token:
            all_token[i]=[unit_id]
            Tokens_Length[i] = 1
        else:
            all_token[i].append(unit_id)
            Tokens_Length[i] += 1
    return

def Document_Process(i):
    processed_document = ""
    i = i.replace("\n","")
    i = re.sub(Titles, "\\1<PERIODATHERE>", i)
    i = i.replace(". ", " ")
    i = i.replace("! ", " ")
    i = i.replace("? ", " ")
    i = i.replace(", ", " ")
    i = i.replace("<PERIODATHERE>", ".")    
    i = re.sub("([A-Za-z])[.]([A-Za-z])[.]([A-Za-z])[.]","\\1PERIODATHERE\\2PERIODATHERE\\3PERIODATHERE",i)
    i = re.sub("([A-Za-z])[.]([A-Za-z])[.]","\\1PERIODATHERE\\2PERIODATHERE",i)
    i = re.sub("([0-9])[.]([0-9])","\\1PERIODATHERE\\2",i)
    i = re.sub('([^\w\s^\'])', r' \1 ', i)
    i = re.sub('\s{2,}', ' ', i)
    i = i.replace("PERIODATHERE", ".")
    words = i.strip(string.punctuation).split(" ")
    for word in words:
        the_word = word
        if the_word in past_tense_and_plural:
                the_word = past_tense_and_plural[the_word]
        the_word = utils.porter_stemmer(the_word)
        if the_word not in string.punctuation:
            processed_document += the_word + " "
    return processed_document

all_token = {}
Tokens_Length = {}
ID_and_Text = {}
data["all_text"] = ""
for index, row in data.iterrows():
    data.loc[index, "all_text"] = (row['headline']+" "+row['text']).replace('</br></br>',' ').lower()
    Word_Tokenization(data.loc[index, "all_text"], data.loc[index, "_unit_id"] )
    ID_and_Text[data.loc[index, "_unit_id"]] = Document_Process(data.loc[index, "all_text"])

os.makedirs(os.path.dirname(args.i+"/"), exist_ok=True)
with open(args.i + '/Posting_List.pkl', 'wb') as f:
    pickle.dump(all_token, f, pickle.HIGHEST_PROTOCOL)
with open(args.i + '/Posting_List_Length.pkl', 'wb') as f:
    pickle.dump(Tokens_Length, f, pickle.HIGHEST_PROTOCOL)
with open(args.i + '/ID_and_Text.pkl', 'wb') as f:
    pickle.dump(ID_and_Text, f, pickle.HIGHEST_PROTOCOL)
print("Index Created!!")

