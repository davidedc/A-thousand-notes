from twitterscraper import query_tweets

if __name__ == '__main__':

    #print the retrieved tweets to the screen:
    for tweet in query_tweets("Trump OR Clinton", 1):
        print(tweet)

