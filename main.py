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
    data = []

    results = tweepy.Cursor(
        api.user_timeline,
        id=user_id,
        tweet_mode='extended'
    ).items()
    
    for status in results:
        tweet='\t'.join([
            status.id_str, 
            format_datetime(status.created_at), 
            status.full_text.replace('\n', '（改行）')
        ])
        data.append(tweet)
    
    print(str(len(data)) + ' tweets found')
    write_tsv(data)


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