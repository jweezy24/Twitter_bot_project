import sys
import nltk.tokenize as nt
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk
import multiprocessing as mp
from functools import partial
from tiny_db_calls import *
from graph_data_structure import *
sys.path.append('../src')
from server.db_controller import *




types_of_words_to_filter = ['NNS', 'NN', 'NNP', 'NNPS']
ignored_words = stopwords.words('english')
bad = os.environ['BADWORDSPATH']
if bad != "":
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
def filter_out_words(data, mongo=False, debug=False):
    out = {}
    context = {}
    topics = {}
    for row in data:
        if not mongo:
            text = row["text"]
        else:
            text = row.text
        polarity = "pos" if determine_sentiment_of_text(text) else "neg"
        ss=nt.sent_tokenize(text)
        tokenized_sent=[nt.word_tokenize(sent) for sent in ss]
        pos_sentences=[nltk.pos_tag(sent) for sent in tokenized_sent]
        if type(row) == type({}):
            if "context_annotations" in row.keys():
                for item in row["context_annotations"]:
                    if 'entity' in item.keys():
                        if 'description' in item['entity'].keys():
                            if item['entity']['description'] in context:
                                if polarity == "pos":
                                    context[item['entity']['description']] += 1
                                elif polarity == "neg":
                                    context[item['entity']['description']] -= 1
                            else:
                                if polarity == "pos":
                                    context[item['entity']['description']] = 1
                                elif polarity == "neg":
                                    context[item['entity']['description']] = -1

                        if 'name' in item['entity'].keys():
                            if item['entity']['name'] in topics:
                                if polarity == "pos":
                                    topics[item['entity']['name']] += 1
                                elif polarity == "neg":
                                    topics[item['entity']['name']] -= 1
                            else:
                                if polarity == "pos":
                                    topics[item['entity']['name']] = 1
                                elif polarity == "neg":
                                    topics[item['entity']['name']] = -1
        
        elif "context_annotations" in dir(row):
            context_t = row.context_annotations
            for item in context_t:
                if item.entity.description in context and item.entity.description != None:
                    if polarity == "pos":
                        context[item.entity.description] += 1
                    elif polarity == "neg":
                        context[item.entity.description] -= 1
                else:
                    if polarity == "pos":
                        context[item.entity.description] = 1
                    elif polarity == "neg":
                        context[item.entity.description] = -1
        
            
        
        for sentence in pos_sentences:
            for word,w_type in sentence:
                if w_type in types_of_words_to_filter and len(word) > 1 and word_check(word) and "/" not in word:
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

    return out,context,topics

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
    # pretty_print(lst_neg, is_neg=True)
    # pretty_print(lst_pos)
    return lst_pos,lst_neg

'''
This method will rank the contexts the user is most asscociated with.
input:
    data = dictionary of contexts where the indexs are the context and the value at the index is the occurance of that context.
    total = the amount of context the user would like to be ranked.
output:
    out = a list of those words ranked
'''
def rank_context_dictionary(data, total=100):
    lst = []
    lst_neg = []
    if len(data.keys()) < total:
        total = len(data.keys())
    for i in range(0,total):
        local_max = None
        context = ''
        for key in data.keys():
            amount = data[key]
            if (local_max == None or amount > local_max ) and (key,amount) not in lst:
                local_max = amount
                context = key
        lst.append((context,local_max))

    for i in range(0,total):
        local_min = None
        context = ''
        for key in data.keys():
            amount = data[key]
            if (local_min == None or amount < local_min ) and (key,amount) not in lst_neg:
                local_min = amount
                context = key
        lst_neg.append((context,local_min))
    
    return (lst,lst_neg)

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
            print(f"{count}. {i}")
            count+=1
    else:
        lst.reverse()
        count = 1
        for i in lst:
            print(f"{count}. {i}")
            count+=1

'''
This method will combine favorites without context with favorites with context.
input:
    user = Twitter username to combine favorites with context.
output:
    list of favorites where the id with context is prioritized.
'''
def combine_favorites_with_context(user, Mongo=True):
    #This method will be another sorting algorithm

    #Grab Mongo data or use local json caches
    #initalization of two lists
    if Mongo:
        u = get_account(user)
        favs = u.favorite_tweets
        favs_context = u.favorite_context
    else:
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

    favs_tmp = []
    favs_c_tmp = []
    
    for tweet in favs:
        tmp = int(tweet["id"])
        favs_ids.append(tmp)
        favs_tmp.append(tmp)

    for tweet in favs_context:
        #The API we built has ids as strings rather than integers
        tmp = int(tweet["id"])
        favs_context_ids.append(tmp)
        favs_c_tmp.append(tmp)

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
        
        if h1 and not h2:
            ele = (h1, 0)
            h1 = None
        
        elif h2 and not h1:
            ele = (h2, 1)
            h2 = None

        elif h1 < h2:
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
            ind = favs_tmp.index(id)
            final.append(favs[ind])
        if lst == 1:
            ind = favs_c_tmp.index(id)
            final.append(favs_context[ind])

    return final


'''
This method will combine user's tweets without context with tweets with context.
input:
    user = Twitter username to combine tweets with context.
output:
    list of tweets where the id with context is prioritized.
'''
def combine_tweets_with_context(user, Mongo=True):
    #This method will be another sorting algorithm

    #intialization of two lists that we would like to merge.
    if not Mongo:
        all_tweets = get_all_table_entries(user, table="tweets")
        tweets_context = get_all_table_entries(user, table="tweets_context")
    else:
        #grab Mongodb data
        u = get_account(user)
        all_tweets = u.tweets
        tweets_context = u.tweets_context

    ''' MERGING ALGORITHM DESCRIPTION '''
    #We want to merge by tweet id.
    #Both lists in the initalization will be different sizes.
    #So, we will have to approach the problem by copying all of the ids by themselves into two lists
    #We then search for numbers that match.
    #If the numbers do not match we take the entry from favs.
    #If there exists a match we use the entry from tweets_context
    

    #Create the id arrays
    tweet_ids = []
    tweet_context_ids = []
    tweet_tmp = []
    tweet_context_tmp = []
    
    for tweet in all_tweets:
        tmp = int(tweet["id"])
        tweet_ids.append(tmp)
        tweet_tmp.append(tmp)
    
    for tweet in tweets_context:
        #The API we built has ids as strings rather than integers
        tmp = int(tweet["id"])
        tweet_context_ids.append(tmp)
        tweet_context_tmp.append(tmp)

    #Sort the lists we gathered
    tweet_ids.sort()
    tweet_context_ids.sort()
    #inits
    h1 = None
    h2 = None
    ele = None
    ids = []
    
    # Merge the lists
    # In the algorithm below we will treat the lists above as queues
    # Algorithm pseudocode https://en.wikipedia.org/wiki/Merge_algorithm
    while len(tweet_ids) != 0 or len(tweet_context_ids) != 0:
        if not h1 and len(tweet_ids) > 0:
            h1 = tweet_ids.pop(0)
        
        if not h2 and len(tweet_context_ids) > 0:
            h2 = tweet_context_ids.pop(0)
        
        
        if h1 and not h2:
            ele = (h1, 0)
            h1 = None
        
        elif h2 and not h1:
            ele = (h2, 1)
            h2 = None

        elif h1 < h2:
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
            ind = tweet_tmp.index(id)
            final.append(all_tweets[ind])
        
        elif lst == 1:
            ind = tweet_context_tmp.index(id)
            final.append(tweets_context[ind])

    return final


def word_check(word):
    for bword in ignored_words:
        if word.lower().strip() == bword.lower().strip():
            return False
    return True


'''
This algorithm will determine the distance between users based on tweets associated with them.
input:
    root_user = The user that we want to act as the center
output:
    A dictionary which has each cached user's distance from the root_user
'''
def distance_algorithm_calculation(root_user):

    ''' 
    For the distance calculation, we want to gather the top 100 most used words from their tweets and favorites.
    '''

    ''' The first thing we want to do is gather up the users we have saved in the database.
    These users are connected the the main user by either following them or the root_user follows them.
    '''
    #Inits of the followers and following
    followers = [i["id"] for i in get_all_table_entries(root_user, "followers")]
    following = [i["id"] for i in get_all_table_entries(root_user, "following")]

    #List of users we want to gather their data for

    to_check = followers + following

    

    # for root, dirs, files in os.walk(os.environ["TINYDB_PATH"], topdown=False):
    #     for name in files:
    #         user = name.replace(".json", "")
    #         if user in followers or user in following:
    #             to_check.append(user)

    
    base_favorites = combine_favorites_with_context(root_user)
    base_tweets = combine_tweets_with_context(root_user)
    base_all_tweets = base_favorites+base_tweets
    
    #We want to user this dictionary data structure to cache all text assoicated with a user
    data_cache = {}

    for user in to_check:
        u = get_account(user)
        if u is not None:
            data_cache.update({user: u})
    
    base_words, base_contexts, base_topics = filter_out_words(base_all_tweets)
    base_ranked_words_pos,base_ranked_words_neg = rank_words_dictionary(base_words)
    base_ranked_words = base_ranked_words_pos + base_ranked_words_neg
    base_ranked_context_pos, base_ranked_context_neg = rank_context_dictionary(base_contexts)
    base_ranked_context = base_ranked_context_pos + base_ranked_context_neg
    base_ranked_topics_pos,base_ranked_topics_neg = rank_context_dictionary(base_topics)
    base_ranked_topics = base_ranked_topics_pos,base_ranked_topics_neg

    words_t = []
    weight_t = []
    words_w = [ i[0] for i in base_ranked_words]
    words_c = [ i[0] for i in base_ranked_context]
    if len(base_ranked_topics[0]) > 0:
        words_t = [ i[0] for i in base_ranked_topics]
    else:
        words_t = []
    weight_w = [ i[2] for i in base_ranked_words]
    weight_c = [ i[1] for i in base_ranked_context]
    if len(base_ranked_topics[1]) > 0:
        weight_t = [ i[1] for i in base_ranked_topics]
    else:
        weight_t = []
    weighted_users = []

    manager = mp.Manager()
    return_dict = manager.dict()
    cutoff = 5 ##
    processes = []
    count = 0
    for key in data_cache.keys():
        val = mp.Process(target=calculate_weight, args=(key, data_cache,(words_w,weight_w), (words_c,weight_c),(words_t,weight_t),return_dict,) )
        val.start()
        processes.append(val)
        count+=1
        if cutoff < count:
            for process in processes:
                process.join()
            count = 0
    for process in processes:
        process.join()
    
    weighted_users = return_dict.values()
    print(weighted_users)
    return weighted_users


def calculate_weight(key, data_cache,base_rw,base_rc,base_rt,returns):
    tweets = combine_tweets_with_context(key)
    words, contexts, topics = filter_out_words(tweets, mongo=True, debug=True)
    #print(contexts)
    user = key
    x = 0
    y = 0
    give_weight = False
    for key in words.keys():
        word,tp = key
        wgt = words[key]
        
        wgt = get_weight_of_word(base_rw[0], base_rw[1], word, wgt)
        x += wgt
        give_weight = True
    
    for key in contexts.keys():
        word = key
        wgt = contexts[key]

        wgt = get_weight_of_word(base_rc[0], base_rc[1], word, wgt)  
        y += wgt
        give_weight = True

    for keys in topics.keys():
        word = key
        wgt = topics[key]

        wgt = get_weight_of_word(base_rt[0], base_rt[1], word, wgt)
        y += wgt
        give_weight = True
    
    x = after_collation_weights(x,base_rw,words)
    y = after_collation_weights(y,base_rc,contexts)
    y = after_collation_weights(y,base_rt,topics)

    if give_weight:
        returns.update({user:(user,x, y)})
        

def get_weight_of_word(words, weights, word, weight):

    if word in words:
        ind = words.index(word)
        wgt = weights[ind]
        return wgt-weight

    else:
        return weight

def after_collation_weights(x,b,b2):
    count = 0
    b_w = b[0]
    b_w2 = b[1]
    for word in b_w:
        if word not in b2.keys():
            wgt = b_w2[count]
            x -= wgt
        count+=1
    
    return x

if __name__ == "__main__":
    print(distance_algorithm_calculation('jack_west24'))