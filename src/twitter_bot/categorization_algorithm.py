import nltk.tokenize as nt
import nltk

types_of_words_to_filter = ['NNS', 'NN', 'NNP', 'NNPS', 'VB','VBD','VBG','VBN','VBP','JJ', 'JJR', 'JJS']

'''
This method creates a dictionary which indexs by word and the value at the index is word classification and amount of occurances.
input:
    data = list of json entries 
output:
    out = dictionary of words with the word's type and occurances.
'''
def filter_out_words(data):
    out = {}
    for row in data:
        text = row["text"]
        ss=nt.sent_tokenize(text)
        tokenized_sent=[nt.word_tokenize(sent) for sent in ss]
        pos_sentences=[nltk.pos_tag(sent) for sent in tokenized_sent]
        for sentence in pos_sentences:
            for word,w_type in sentence:
                if w_type in types_of_words_to_filter and len(word) > 1:
                    if (word.lower(),w_type) in out:
                        out[(word.lower(),w_type)] = out[(word.lower(),w_type)] + 1
                    else:
                        out[(word.lower(),w_type)] = 1
    return out

'''
This method will rank each word found in a given dictionary.
First, we sort each word by useage.
input:
    data = dictionary of words where the indexs are the word and type as the method above would create.
    total = the amount of imprant words the user would like to see.
output:
    out = a list of those words ranked
'''
def rank_words_dictionary(data, total=50):
    #Creates a list of empty lists
    lst = [[] for i in range(0,total)]
    #Create a copy of the dictionary given such that we can alter the dictionary. 

    totals = list(data.values())
    totals.sort()
    totals.reverse()

    mappings = totals[0:total]

    #For our searching algorithm we are going to use a dynamic programing approach    
    for ind in data.keys():
        if data[ind] in mappings:
            tmp_ind = mappings.index(data[ind])
            
            #if the mapping is already filled i.e the amount has already been used in that position we recursively find the next index.
            def rec_check(ind, lst):
                if ind >= len(lst):
                    return None
                if lst[ind] == []:
                    return ind
                else:
                    return rec_check(ind+1, lst)
            new_ind = rec_check(tmp_ind, lst)
            
            if new_ind != None:
                lst[new_ind] = (ind[0], ind[1], data[ind])


    print(lst)
    return lst
        
        


