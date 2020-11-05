## Elijah Jasso 2020
## This python code is a test file to test out Twint functionality

import twint # import Twitter scraper

# isUserValid
# userID (string): the Twitter ID of the user
# Determination will basically be:
# User must have at least 5 political tweets
def isUserValid(userID):
    print("try to see if user is valid")

    return True


# getTweetAnalysis(tweetText)
# tweetText (string): the text of the tweet
# returns: dictionary of "topic" (string) and "sentiment" (integer)
# if tweet is not political "topic" = None
def getTweetAnalysis(tweetText):
    # currently this is the only thing this will output until I test some machine learning stuff
    tweetDict = {
        "topic": "universal healthcare",
        "sentiment": 0
    }

    return tweetDict


## Function finds users
def getUsers(frontiers = 2, usersPerFrontier = 10, minFollowers = 10, maxFollowers = 450, minFollowing = 10, maxFollowing = 1000, initialTweets = 100):
    print("getData called")
    c = twint.Config()
    c.Limit = 100 # Twint only gets Tweets in the size of 100
    c.Count = True
    c.Search = "vote" # contains this keyword
    c.Since = "2020-11-03" # only output tweets since this date
    c.Verified = False # users should not be verified (blue check mark)
    c.Hide_output = True # don't print output to console here (maybe do it elsewhere)
    c.Debug = True
    c.Store_object = True # store as object
    c.Store_json = True
    c.Output = "initialUsers.json"
    # c.User_full = True
    data = []
    #c.Store_object_tweets_list = data
    twint.run.Search(c)
    #data = twint.output.tweets_list
    return data

# main function that runs when python code is run
if __name__ == "__main__":
    print("main called")
    users = getUsers(2, 10)
    print(len(users))
    # for i in range(10):
    #     print(users[i].username + ": " + users[i].tweet + " --- AT " + users[i].timestamp + " " + users[i].datestamp)

