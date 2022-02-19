def twitterStreamer(kw):
    import tweepy
    import twitter_credentials
    import pandas as pd

    """ Authentication"""
    auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    """ Streaming from twitter"""

    class Listener(tweepy.Stream):

        tweets = []
        limit = 100

        def on_status(self, status):
            self.tweets.append(status)

            if len(self.tweets) == self.limit:
                self.disconnect()

    stream_tweet = Listener(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET,
                            twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    # Stream by keywords

    keywords = kw

    stream_tweet.filter(track=keywords, filter_level=["low"], languages=["en"])

    # create DataFrame

    columns = ['Tweets']
    data = []

    for tweet in stream_tweet.tweets:
        if not tweet.truncated:
            data.append([tweet.text])
        else:
            data.append([tweet.extended_tweet['full_text']])

    df = pd.DataFrame(data, columns=columns)
    df = df[~df.Tweets.str.contains("RT")]

    print(df)
    df.to_csv('tweets.csv')
