# Twitter Categorization Bot 
### COMP 460 Project
### Group Members: David Gubala, Yandi Farinango, Piotr Jackowski, Andrew Littleton, Neha Patel, Jack West

## Project Description
The Twitter Categorization Bot (TCB) is designed to gather information from a root Twitter account and a deliver rudimentary estimation of the user’s connections and cultural associations. We have dubbed this a person's: *Twitter Universe*. Using words, topics, and similarities between the root account and accounts connected to it, the TCB can provide a reasonable assumption of a twitter user's "personality". 
Information gathered:
- Tweets
- Favorites
- Followers
- Associated Topics 

While a user's personality, even when limiting the scope of interest to one social media platform, is ultimately very complex and requires extensive amounts of information gathering and analysis, a foundational analysis can be determined. We have decided on the information categories above because they provide the most foundational part of a person's Twitter Universe.

## Twitter API 
### Considerations
##### Twitter API Limits
The rate limit for twitter's calls are category specific.
Meaning, that if you only want to collect favorites of a specific user, getting the favorites shouldn't interfer with getting the user's followers.
Although, there is a an extremely small amount of calls regardless of the lack of intersections calls could potientally have. Some calls will allow for `500` calls while others allow for `900`. Therefore, designing the API usage methods will require a different timing allocation for calls. After examining two Python libraries that accomplish the same task to see which one had better API rates, we can optimize the API calls.
##### Time
This problem stems from the API call limit per amount of time. We are limited to '500' calls per 15 minutes. Due to lack of calls, time to generate a visualization could take longer than intended. This could be extended for longer time frames depending on the API calls.
### Research
### Usage
The Twitter API is the primary method the TCB uses to gather information about twitter accounts. A server running a background REST process consistently builds a database of user data for a graph to be built later. The data gathering algorithm starts with an arbitrary user and gathers the necessary information related to that user. The data gathering server runs 24/7 and paces itself with the Twitter API call rate so that the algorithm will not break due to time constraints.
## Categorization Algroithm
### Research
## Front End Display Algorithm
### Research
## Data Analysis
## Conclusion


