import datetime
import os

import pytz
import tweepy


# TwitterAPI
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

timezone = pytz.timezone('Asia/Tokyo')


def get_all_tweets(user_id):
    api = oauth()
    rows = []

    tweets = tweepy.Cursor(
        api.user_timeline,
        id=user_id,
        tweet_mode='extended'
    ).items()
    
    for tweet in tweets:
        row='\t'.join([
            tweet.id_str, 
            format_datetime(tweet.created_at), 
            tweet.full_text.replace('\n', '（改行）')
        ])
        rows.append(row)
    
    print(str(len(rows)) + ' tweets found')
    write_tsv(rows)


def oauth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


def write_tsv(data):
    with open('tweets.tsv','w') as f:
        f.write('\n'.join(data))


def format_datetime(dt):
    return timezone.fromutc(dt).strftime('%Y-%m-%d_%H:%M:%S')


if __name__ == '__main__':
    get_all_tweets(input())