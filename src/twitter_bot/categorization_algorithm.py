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
                if (word,w_type) in out:
                    out[(word,w_type)] = out[(word,w_type)] + 1
                else:
                    out[(word,w_type)] = 1

    return out


