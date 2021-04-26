[![Build Status](https://travis-ci.com/jweezy24/Twitter_bot_project.svg?branch=main)](https://travis-ci.com/github/jweezy24/Twitter_bot_project)
# TCB: Twitter Categorization Bot


See TwitterBotProject.md for project report.


## Installation

OS X & Linux:

Debian:

```
sudo apt install python3
```

Arch:

```
sudo pacman -Sy python python-pip 
```




## Development setup

To install all dependencies run the command below. We also require python3. 

```
pip install -r ./requirements.txt
```

You will also need some tokens within a environment variable `APIKEY`, `APISECRET`, `TWITTERUSER`, `TWITTERPASS`, `BEARER`, `TINYDB_PATH`, and `BADWORDSPATH`  to properly run the python twitter bot code.

One of the dependencies is the [Natural Language Toolkit](https://www.nltk.org/)(NLTK).
There are some files that are needed to use NLTK that you would have to download.
To install those files, run the command below,

```
python3 setup.py
```



## Authors

Jack West – [@GitHub](https://github.com/jweezy24) - Jwest1@luc.edu 

Andrew Littleton - [@Github](https://github.com/alittleton98) - admin@andrewlittleton.com

Piotr Jackowski - [@Github](https://github.com/pjack7oo) - pjackowski@luc.edu
Yandi Farinango - [@Github](https://github.com/yandi-farinango) - yfarinango@luc.edu

[README Template](https://github.com/dbader/readme-template)



