## Summary

We use two twitter API libraries that are built into python's pip package manager.
Although, we built our own methods that parse data from the api methods into manageable ways.
Below is the documentation of said methods.
To developers, below will also be an explaination of the limiations of the twitter API.

## Limitations

**There are only 900 API calls every 15 minutes**

The limitation of these calls means every single call will matter.
Also, users with over 500 followers will not be able to see all of their followers within our data visualization.
To deal with this we should grab all the followers and somehow figure out what is going 

## How to use NLTK Word Lists

Here is the full POS tag list:

CC 	coordinating conjunction
CD	 cardinal digit
DT 	determiner
EX	existential there (like: "there is" ... think of it like "there exists")
FW  	foreign word
IN  	preposition/subordinating conjunction
JJ 	adjective    'big'
JJR	adjective, comparative    'bigger'
JJS	adjective, superlative    'biggest'
LS	List marker    1)
MD	modal    could, will
NN	noun, singular 'desk'
NNS	 noun plural    'desks'
NNP	proper noun, singular    'Harrison'
NNPS	 proper noun, plural    'Americans'
PDT	predeterminer    'all the kids'
POS	possessive ending    parent's
PRP	personal pronoun    I, he, she
PRP$	 possessive pronoun    my, his, hers
RB	adverb    very, silently,
RBR	adverb, comparative    better
RBS	Adverb, superlative    best
RP	particle    give up
TO	to go 'to' the store.
UH	 interjection    errrrrrrrm
VB	Verb, base form    take
VBD	verb, past tense, took
VBG	Verb, gerund/present participle    taking
VBN	verb, past participle taken
VBP	verb, sing. present, non-3d    take
VBZ	 verb, 3rd person sing. present    takes
WDT	wh-determiner  which
WP	 wh-pronoun    who, what
WP$	possessive wh-pronoun    whose
WRB	wh-adverb    where, when

This list is how NLTK categorizes words.
We can determine which word is imporant and could lead to defining who a person is.

## What Tweepy and Twitter.py are missing.

Both well known APIs do not support the context annotations requests.
These are important as they are the categorizations that we wanted to fully focus on.
So, one of the things that we had to do was build out those API requests.


## Positive Words list Notes

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; 
; Opinion Lexicon: Positive
;
; This file contains a list of POSITIVE opinion words (or sentiment words).
;
; This file and the papers can all be downloaded from 
;    http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
;
; If you use this list, please cite one of the following two papers:
;
;   Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
;       Proceedings of the ACM SIGKDD International Conference on Knowledge 
;       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
;       Washington, USA, 
;   Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
;       and Comparing Opinions on the Web." Proceedings of the 14th 
;       International World Wide Web conference (WWW-2005), May 10-14, 
;       2005, Chiba, Japan.
;
; Notes: 
;    1. The appearance of an opinion word in a sentence does not necessarily  
;       mean that the sentence expresses a positive or negative opinion. 
;       See the paper below:
;
;       Bing Liu. "Sentiment Analysis and Subjectivity." An chapter in 
;          Handbook of Natural Language Processing, Second Edition, 
;          (editors: N. Indurkhya and F. J. Damerau), 2010.
;
;    2. You will notice many misspelled words in the list. They are not 
;       mistakes. They are included as these misspelled words appear 
;       frequently in social media content. 
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;