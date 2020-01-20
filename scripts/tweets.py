import os
import pandas as pd
import tweepy as tw

#Script used for Tweets scraping

consumer_key = ''
consumer_secret_key = ''
access_token = ''
access_token_secret = ''

auth = tw.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "from:nytpolitics -filter:retweets"
date_since = "2019-10-6"

# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'politics'
print(df.head(10))

df.to_csv(r'nytpoliticstweets.csv', index=None, header=True)

# ---------------------

search_words = "from:CNNPolitics -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'politics'
print(df.head(10))

df.to_csv(r'CNNPoliticstweets.csv', index=None, header=True)

# ------------------

search_words = "from:NYDNPolitics -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'politics'
print(df.head(10))

df.to_csv(r'NYDNPoliticstweets.csv', index=None, header=True)

# --------------------

search_words = "from:sciencemagazine -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'science'
print(df.head(10))

df.to_csv(r'sciencemagazinetweets.csv', index=None, header=True)

# --------------------

search_words = "from:NASA -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'science'
print(df.head(10))

df.to_csv(r'NASAtweets.csv', index=None, header=True)

# --------------------

search_words = "from:naturenews -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'science'
print(df.head(10))

df.to_csv(r'naturenewstweets.csv', index=None, header=True)

# --------------------

search_words = "from:techreview -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'tech'
print(df.head(10))

df.to_csv(r'techreviewtweets.csv', index=None, header=True)

# --------------------

search_words = "from:techcohq -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'tech'
print(df.head(10))

df.to_csv(r'techcohqtweets.csv', index=None, header=True)

# --------------------

search_words = "from:RNS -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'religion'
print(df.head(10))

df.to_csv(r'RNStweets.csv', index=None, header=True)

# --------------------

search_words = "from:CNNbelief -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'religion'
print(df.head(10))

df.to_csv(r'CNNbelieftweets.csv', index=None, header=True)


# --------------------

search_words = "from:BBCSport -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'sport'
print(df.head(10))

df.to_csv(r'BBCSporttweets.csv', index=None, header=True)

# --------------------

search_words = "from:Motor_Sport -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'sport'
print(df.head(10))

df.to_csv(r'Motor_Sporttweets.csv', index=None, header=True)

# --------------------

search_words = "from:guardian_sport -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'sport'
print(df.head(10))

df.to_csv(r'guardian_sporttweets.csv', index=None, header=True)


# --------------------

search_words = "from:youtubemusic -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'music'
print(df.head(10))

df.to_csv(r'youtubemusictweets.csv', index=None, header=True)

# --------------------

search_words = "from:BBCR1 -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'music'
print(df.head(10))

df.to_csv(r'BBCR1tweets.csv', index=None, header=True)

# --------------------

search_words = "from:mtvema -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'music'
print(df.head(10))

df.to_csv(r'mtvematweets.csv', index=None, header=True)

# --------------------

search_words = "from:UMG -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'music'
print(df.head(10))

df.to_csv(r'UMGtweets.csv', index=None, header=True)

# Cinema
# --------------------

search_words = "from:IMDb -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'cinema'
print(df.head(10))

df.to_csv(r'IMDbtweets.csv', index=None, header=True)

# --------------------

search_words = "from:netflix -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'cinema'
print(df.head(10))

df.to_csv(r'netflixtweets.csv', index=None, header=True)

# --------------------

search_words = "from:paramountnet -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'cinema'
print(df.head(10))

df.to_csv(r'paramountnettweets.csv', index=None, header=True)

# --------------------

search_words = "from:Dreamworks -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode="extended").items(10000)

attributes = [[tweet.user.screen_name, tweet.full_text, tweet.user.location, tweet.created_at] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'cinema'
print(df.head(10))

df.to_csv(r'Dreamworkstweets.csv', index=None, header=True)

# --------------------

'''
search_words = "from:21CF -filter:retweets"
# Collect tweets
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since).items(10000)

attributes = [[tweet.user.screen_name, tweet.text, tweet.user.location] for tweet in tweets]

df = pd.DataFrame(data=attributes, columns=['user', 'text', 'location', 'date'])
df['topic'] = 'cinema'
print(df.head(10))

df.to_csv(r'21CFtweets.csv', index=None, header=True)
'''

