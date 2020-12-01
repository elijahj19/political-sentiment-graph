import twitter_wrapper as tw

username = 'c3smoorevp'

userFollowers = tw.getFollowers(username)
print(userFollowers)
print(len(userFollowers))

userFollowing = tw.getFollowing(username)
print(userFollowing)
print(len(userFollowing))

