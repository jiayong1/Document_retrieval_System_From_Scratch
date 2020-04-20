
# coding: utf-8

# In[ ]:
import re
import string

Titles = "(Mr|Mrs|Ms|Dr|Inc|Ltd|Jr|Sr|Co)[.]"
vowel = ["a", "e", "i", "o", "u"]
def Get_M(word):
    form = ""
    for i in word:
        if i in vowel:
            form +="1"
        else:
            form += "0"
    form = re.sub(r'(\d)\1+', r'\1', form)       
    return form.count("10")

def porter_stemmer(word):
    word = word.lower()
    if word == "as":
        return word
    #Setp 1a
    if word[-4:] == "sses":
        word = word[:-4] + "ss"
    elif word[-3:] == "ies":
        word =  word[:-3] + "i"
    elif word[-2:] == "ss":
        word =  word
    elif word[-1:] == "s":
        word =  word[:-1]
    
    #Step 1b
    go_to_special = False
    if Get_M(word[:-3]) > 0 and word[-3:] == "eed":
        word =  word[:-3] + "ee"
    elif ("a" in word[:-2] or "e" in word[:-2] or "i" in word[:-2] or "o" in word[:-2] or "u" in word[:-2]) and word[-2:] == "ed":
        word = word[:-2]
        go_to_special = True
    elif ("a" in word[:-3] or "e" in word[:-3] or "i" in word[:-3] or "o" in word[:-3] or "u" in word[:-3]) and word[-3:] == "ing":
        word = word[:-3]
        go_to_special = True
    if go_to_special:
        if word[-2:] == "at" or word[-2:] == "bl" or word[-2:] == "iz" :
            word =  word + "e"
        elif len(word) >= 2 and (word[-1] == word[-2]) and (word[-1] not in ["l", "s", "z"]):
            word =  word[:-1]
        elif len(word) >= 3 and( Get_M(word) == 1) and (word[-1] not in vowel) and (word[-2] in vowel) and (word[-3] not in vowel) and (word[-1] not in ["w","x","y"]):
            word =  word +"e"
    
    #step 1c
    if ("a" in word[:-1] or "e" in word[:-1] or "i" in word[:-1] or "o" in word[:-1] or "u" in word[:-1]) and word[-1] == "y":
        word = word[:-1] + "i"
    # step 2
    if (Get_M(word[:-7]) >0) and  word[-7:] == "ational":
        word = word[:-7]+ "ate"
    elif (Get_M(word[:-6]) >0) and word[-6:] == "tional":
        word = word[:-6]+ "tion"
    elif (Get_M(word[:-4]) >0) and word[-4:] == "enci":
        word = word[:-4]+ "ence"
    elif (Get_M(word[:-4]) >0) and word[-4:] == "anci":
        word = word[:-4]+ "ance"
    elif (Get_M(word[:-4]) >0) and word[-4:] == "izer":
        word = word[:-4]+ "ize"
    elif (Get_M(word[:-4]) >0) and word[-4:] == "abli":
        word = word[:-4]+ "able"
    elif (Get_M(word[:-4]) >0) and word[-4:] == "alli":
        word = word[:-4]+ "al"
    elif (Get_M(word[:-5]) >0) and word[-5:] == "entli":
        word = word[:-5]+ "ent"
    elif (Get_M(word[:-3]) >0) and word[-3:] == "eli":
        word = word[:-3]+ "e" 
    elif (Get_M(word[:-5]) >0) and word[-5:] == "ousli":
        word = word[:-5]+ "ous"
    elif (Get_M(word[:-7]) >0) and word[-7:] == "ization":
        word = word[:-7]+ "ize"
    elif (Get_M(word[:-5]) >0) and word[-5:] == "ation":
        word = word[:-5]+ "ate"
    elif (Get_M(word[:-4]) >0) and word[-4:] == "ator":
        word = word[:-4]+ "ate"
    elif (Get_M(word[:-5]) >0) and word[-5:] == "alism":
        word = word[:-5]+ "al"
    elif (Get_M(word[:-7]) >0) and word[-7:] == "iveness":
        word = word[:-7]+ "ive"
    elif (Get_M(word[:-7]) >0) and word[-7:] == "fulness":
        word = word[:-7]+ "ful"
    elif (Get_M(word[:-7]) >0) and word[-7:] == "ousness":
        word = word[:-7]+ "ous"
    elif (Get_M(word[:-5]) >0) and word[-5:] == "aliti":
        word = word[:-5]+ "al"
    elif (Get_M(word[:-5]) >0) and word[-5:] == "iviti":
        word = word[:-5]+ "ive"
    elif (Get_M(word[:-6]) >0) and word[-6:] == "biliti":
        word = word[:-6]+ "ble"
# step 3
    if (Get_M(word[:-5]) >0) and word[-5:] == "icate":
        word = word[:-5]+ "ic"
    elif (Get_M(word[:-5]) >0) and word[-5:] == "ative":
        word = word[:-5]
    elif (Get_M(word[:-5]) >0) and word[-5:] == "alize":
        word = word[:-5] +"al"
    elif (Get_M(word[:-5]) >0) and word[-5:] == "iciti":
        word = word[:-5] +"ic"
    elif (Get_M(word[:-4]) >0) and word[-4:] == "ical":
        word = word[:-4] +"ic"
    elif (Get_M(word[:-3]) >0) and word[-3:] == "ful":
        word = word[:-3] 
    elif (Get_M(word[:-4]) >0) and word[-4:] == "ness":
        word = word[:-4]
    # step 4
    if (Get_M(word[:-2]) >1) and word[-2:] == "al":
        word = word[:-2]
    elif (Get_M(word[:-4]) >1) and word[-4:] == "ance":
        word = word[:-4]
    elif (Get_M(word[:-4]) >1) and word[-4:] == "ence":
        word = word[:-4]
    elif (Get_M(word[:-2]) >1) and word[-2:] == "er":
        word = word[:-2]
    elif (Get_M(word[:-4]) >1) and word[-4:] == "ance":
        word = word[:-4]
    elif (Get_M(word[:-2]) >1) and word[-2:] == "ic":
        word = word[:-2]
    elif (Get_M(word[:-4]) >1) and word[-4:] == "able":
        word = word[:-4]
    elif (Get_M(word[:-4]) >1) and word[-4:] == "ible":
        word = word[:-4]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "ant":
        word = word[:-3]
    elif (Get_M(word[:-5]) >1) and word[-5:] == "ement":
        word = word[:-5]
    elif (Get_M(word[:-4]) >1) and word[-4:] == "ment":
        word = word[:-4]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "ent":
        word = word[:-3]
    elif (Get_M(word[:-3]) >1) and len(word) >= 4 and ((word[-4] == "s") or (word[-4] == "t")) and word[-3:] == "ion":
        word = word[:-3]
    elif (Get_M(word[:-2]) >1) and word[-2:] == "ou":
        word = word[:-2]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "ism":
        word = word[:-3]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "ate":
        word = word[:-3]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "iti":
        word = word[:-3]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "ous":
        word = word[:-3]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "ive":
        word = word[:-3]
    elif (Get_M(word[:-3]) >1) and word[-3:] == "ize":
        word = word[:-3]
        
    # step 5a
    if (Get_M(word[:-1]) >1) and word[-1] == "e":
        word = word[:-1]
    if (len(word) >= 4) and (Get_M(word[:-1]) == 1)  and not ((word[-2] not in vowel) and (word[-3] in vowel) and (word[-4] not in vowel) and (word[-1] not in ["w","x","y"])) and word[-1] == "e":
        word = word[:-1]
    # step 5b
    if (len(word) >= 2) and (Get_M(word) == 1) and word[-1] == word[-2] and word[-1] == "l":
        word = word[:-1] 
    return word

