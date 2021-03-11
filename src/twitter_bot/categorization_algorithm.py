import nltk.tokenize as nt
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk
from tiny_db_calls import *


types_of_words_to_filter = ['NNS', 'NN', 'NNP', 'NNPS']
ignored_words = stopwords.words('english')
bad = "/home/jweezy/Documents/Twitter_bot_project/src/data/badwords.txt"
with open(bad,"r") as f:
    for word in f:
        ignored_words.append(word.strip())

'''
This method creates a dictionary which indexs by word and the value at the index is word classification and amount of occurances.
input:
    data = list of json entries 
output:
    out = dictionary of words with the word's type and occurances.
'''
def filter_out_words(data):
    out = {}
    context = {}
    for row in data:
        text = row["text"]
        polarity = "pos" if determine_sentiment_of_text(text) else "neg"
        ss=nt.sent_tokenize(text)
        tokenized_sent=[nt.word_tokenize(sent) for sent in ss]
        pos_sentences=[nltk.pos_tag(sent) for sent in tokenized_sent]
        if "context_annotations" in row.keys():
            for item in row["context_annotations"]:
                if 'entity' in item.keys():
                    print(item)
                    if 'description' in item['entity'].keys():
                        if item['entity']['description'] in context:
                            context[item['entity']['description']] += 1
                        else:
                            context[item['entity']['description']] = 1
                    if 'name' in item['entity'].keys():
                        if item['entity']['name'] in context:
                            context[item['entity']['name']] += 1
                        else:
                            context[item['entity']['name']] = 1
        for sentence in pos_sentences:
            for word,w_type in sentence:
                if w_type in types_of_words_to_filter and len(word) > 1 and word not in ignored_words:
                    ele = (word.lower(), w_type)
                    if ele in out:
                        if polarity == "neg":
                            out[ele] = out[ele] - 1
                        if polarity == "pos":
                            out[ele] = out[ele] + 1
                    else:
                        if polarity == "neg":
                            out[ele] = -1
                        if polarity == "pos":
                            out[ele] = 1

    return out,context

'''
This method will rank each word found in a given dictionary.
First, we sort each word by useage.
input:
    data = dictionary of words where the indexs are the word and type as the method above would create.
    total = the amount of imprant words the user would like to see.
output:
    out = a list of those words ranked
'''
def rank_words_dictionary(data, total=100):
    #Creates a list of empty lists
    lst_pos = [[] for i in range(0,total)]
    lst_neg = [[] for i in range(0,total)]
    #Create a copy of the dictionary given such that we can alter the dictionary. 

    totals = [i for i in data.values()]
    totals.sort()
    totals.reverse()

    mappings_pos = totals[0:total]
    mappings_neg = totals[len(totals)-total:]

    #For our searching algorithm we are going to use a dynamic programing approach    
    for ind in data.keys():
        if data[ind] in mappings_pos:
            tmp_ind = mappings_pos.index(data[ind])
            
            #if the mapping is already filled i.e the amount has already been used in that position we recursively find the next index.
            def rec_check(ind, lst):
                if ind >= len(lst):
                    return None
                
                if lst[ind] == []:
                    return ind
                else:
                    return rec_check(ind+1, lst)
            
            new_ind = rec_check(tmp_ind, lst_pos)
            
            if new_ind != None:
                lst_pos[new_ind] = (ind[0], ind[1], data[ind], "pos")

        if data[ind] in mappings_neg:
            tmp_ind = mappings_neg.index(data[ind])
            
            #if the mapping is already filled i.e the amount has already been used in that position we recursively find the next index.
            def rec_check(ind, lst):
                if ind >= len(lst):
                    return None
                
                if lst[ind] == []:
                    return ind
                else:
                    return rec_check(ind+1, lst)
            
            new_ind = rec_check(tmp_ind, lst_neg)
            
            if new_ind != None:
                lst_neg[new_ind] = (ind[0], ind[1], data[ind], "neg")
    pretty_print(lst_neg, is_neg=True)
    pretty_print(lst_pos)
    return lst_pos

'''
This method will rank the contexts the user is most asscociated with.
input:
    data = dictionary of contexts where the indexs are the context and the value at the index is the occurance of that context.
    total = the amount of context the user would like to be ranked.
output:
    out = a list of those words ranked
'''
def rank_context_dictionary(data, total=10):
    lst = []

    for i in range(0,total):
        local_max = 0
        context = ''
        for key in data.keys():
            amount = data[key]
            if amount > local_max and (key,amount) not in lst:
                local_max = amount
                context = key
        lst.append((context,local_max))
    
    return lst

'''
This method will determine the polarity of a tweet.
input:
    text = The tweet we wish to determine polarity of.
output:
    True if positive, False if negative
'''

def determine_sentiment_of_text(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)["compound"] >= 0


def pretty_print_context(lst):
    count = 1
    for c,a in lst:
        print(f"{count}. {c}\t{a}")
        count+=1

def pretty_print(lst, is_neg=False):
    if not is_neg:
        count = 1
        for i in lst:
            print(f"{count}. {i[0]}\t {i[1]}\t {i[2]}")
            count+=1
    else:
        lst.reverse()
        count = 1
        for i in lst:
            print(f"{count}. {i[0]}\t {i[1]}\t {i[2]}")
            count+=1

'''
This method will combine favorites without context with favorites with context.
input:
    user = Twitter username to combine favorites with context.
output:
    list of favorites where the id with context is prioritized.
'''
def combine_favorites_with_context(user):
    #This method will be another sorting algorithm

    #intialization of two lists that we would like to merge.
    favs = get_all_favorites(user, table="favorite_tbl")
    favs_context = get_all_favorites(user, table="favorites_context")

    ''' MERGING ALGORITHM DESCRIPTION '''
    #We want to merge by tweet id.
    #Both lists in the initalization will be different sizes.
    #So, we will have to approach the problem by copying all of the ids by themselves into two lists
    #We then search for numbers that match.
    #If the numbers do not match we take the entry from favs.
    #If there exists a match we use the entry from favs_context
    

    #Create the id arrays
    favs_ids = []
    favs_context_ids = []
    
    for tweet in favs:
        favs_ids.append(tweet["id"])
    
    for tweet in favs_context:
        #The API we built has ids as strings rather than integers
        favs_context_ids.append(int(tweet["id"]))

    #Sort the lists we gathered
    favs_ids.sort()
    favs_context_ids.sort()

    #inits
    h1 = None
    h2 = None
    ele = None
    ids = []
    
    # Merge the lists
    # In the algorithm below we will treat the lists above as queues
    # Algorithm pseudocode https://en.wikipedia.org/wiki/Merge_algorithm
    while len(favs_ids) != 0 or len(favs_context_ids) != 0:
        
        if not h1 and len(favs_ids) > 0:
            h1 = favs_ids.pop(0)
        
        if not h2 and len(favs_context_ids) > 0:
            h2 = favs_context_ids.pop(0)
        
        if h1 < h2 and h1 != None:
            ele = (h1, 0)
            h1 = None
            
        elif h1 == h2:
            ele = (h2, 1)
            h1 = None
            h2 = None
            
        else:
            ele = (h2, 1)
            h2 = None
            

        ids.append(ele)


    #print(ids)

    #init of returned list
    final = []

    #We search through the list and dependign on the idicator flag given in the merge algorithm
    #This may seem slower than quereying the databse but it is actually much faster for some reason.
    #This may be a weakness of tinydb.
    #We should migrate this over to a real database once that is ready.
    for id,lst in ids:
        if lst == 0:
            for tweet in favs:
                if tweet["id"] == id:
                    final.append(tweet)
                    break

        elif lst == 1:
            for tweet in favs_context:
                if tweet["id"] == str(id):
                    final.append(tweet)
                    break
    return final

