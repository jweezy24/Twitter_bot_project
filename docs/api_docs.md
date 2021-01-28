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