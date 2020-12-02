import twitter_wrapper as tw

# tw.loadCache()


username = 'c3smoorevp'

# userFollowers = tw.getFollowers(username)
# #print(userFollowers)
# print(len(userFollowers))

userFollowing = tw.getFollowing(username)
# #print(userFollowing)
print(len(userFollowing))

print(tw.getUserSentiment(username, 'trump'))

# print(tw.getFollowersAndFollowingNums(username))

# print(len(tw.getUserTweetsAboutTopic(username, 'trump')))

tw.saveCache()