import nltk.tokenize as nt
import nltk

types_of_words_to_filter = ['NNS', 'NN', 'NNP', 'NNPS', 'VB','VBD','VBG','VBN','VBP','JJ', 'JJR', 'JJS']

def filter_out_words(text):
    ss=nt.sent_tokenize(text)
    tokenized_sent=[nt.word_tokenize(sent) for sent in ss]
    pos_sentences=[nltk.pos_tag(sent) for sent in tokenized_sent]
    wlist = []
    for sentence in pos_sentences:
        for word,w_type in sentence:
            print(f"WORD = {word}\t w_type={w_type}")
    return wlist


