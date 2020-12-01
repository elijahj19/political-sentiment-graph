from bluebird import BlueBird

cache = {} # cache of usernames to data

def loadCache():
    print('Finding saved cache')

def saveCache():
    print('Saving cache')

def getFollowers(username):
    # check if user is cached already, if so then return followers
    if username in cache and 'followers' in cache[username]:
        return cache[username]['followers']
    
    # perform followers search
    followersObj = BlueBird().get_followers(username)
    followers = []
    for user in followersObj: # user is the user's username
        followers.append(user)

    # save user to cache
    if username in cache:
        cache[username]['followers'] = followers
    else:
        cache[username] = {'followers': followers}

    return followers

def getFollowing(username):
    # check if user is cached already, if so then return following
    if username in cache and 'following' in cache[username]:
        return cache[username]['following']

    # perform following search
    followingObj = BlueBird().get_followings(username)
    following = []
    for user in followingObj: # user is the user's username
        following.append(user)
    
    # save user to cache
    if username in cache:
        cache[username]['following'] = following
    else:
        cache[username] = {'following': following}

    return following