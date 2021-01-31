# Challenges

This file contains all future problems that could arise for development.
If any developers think of a new problem add it here.

## Twitter API Limits

The rate limit for twitter's calls are category specific.
Meaning, that if you only want to collect favorites of a specific user, getting the favorites shouldn't interfer with getting the user's followers.
Although, there is a an extremely small amount of calls regardless of the lack of intersections calls could potientally have.
Some calls will alow for `500` calls whereas, others allow for `900`.
Therefore, designing our API useage methods will require thoughly calls and maybe using a couple differnt python packages to see which has the best ratio of API calls to retrieve data.
We should alos be open to the idea of possibly making our own API to have more control over what is called when.
Making our own API should be a last resort as the time to proply build an API is rather time consuming.

## Time

This problem stems from using the Twitter API.
Due to lack of calls, time to generate a visualization could take a minute.
This minute could be extended for longer time frames depending on our API calls.
Therefore, we need a plan to increase the data that won't directly affect the time to complete of our application.

## Photos

Sometimes a tweet or a favorite is just a photo.
Deciding if were to clasify those would be a challenge and may raise the time to complete a examination of a user by quite a bit.
A solution could be to use package like opencv to try to classify a photo, although it could lead to nothing and/or could skew result of the interpretation of the photo is incorrect.
We could also try to use a machine learning algorithm that classifies a photo in some way.

## Identifying Words

This is a potiental problem, asscoition of a person's name could be used in a positive or negative context.
Therefore, understanding the context of a tweet could be change what category a that tweet falls under.