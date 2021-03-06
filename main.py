import tweepy
import os
import time
import urllib
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
gas_url = os.getenv("GAS_URL")

SLEEP_SECOND = 10  # 秒
FOLLOW_USER_COUNT = 3  # 人
REMOVE_USER_COUNT = 6  # 人


def get_client():
    return tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)


def exec_like(client, user_id):
    """
    最新5件のツイートのうち、いいね数が5以上のものがあればすべていいねする。
    """
    tweet_list = client.get_users_tweets(id=user_id, max_results=5, exclude="retweets,replies", tweet_fields="public_metrics")
    if not tweet_list:
        return
    if not tweet_list.data:
        return
    for tweet in tweet_list.data:
        time.sleep(SLEEP_SECOND)
        id = tweet["id"]
        like_count = tweet["public_metrics"]["like_count"]
        if like_count >= 5:
            try:
                client.like(tweet_id=id)
            except Exception as e:
                print(e)


def exec_follow(client):
    try:
        result = urllib.request.urlopen(gas_url + f"?datanum={FOLLOW_USER_COUNT}")
        user_info_list = json.loads(result.read())
    except Exception as e:
        print(e)
    for user_info in user_info_list:
        client.follow_user(target_user_id=user_info["id"])
        exec_like(client, user_info["id"])
        print(f"follow: {id}")
        time.sleep(SLEEP_SECOND)


def exec_remove(client):
    target_user_id = "1449267500454072321"
    remove_count = 0
    try:
        # フォロー中のユーザが新しい順にとれる
        following_list = client.get_users_following(id=target_user_id, max_results=1000).data
        following_list_reversed = list(reversed(following_list))
        followers_list = client.get_users_followers(id=target_user_id, max_results=1000).data
        followers_id_list = list(map(lambda x: x["id"], followers_list))
        for following_user in following_list_reversed:
            if remove_count >= REMOVE_USER_COUNT:
                break
            if following_user["id"] not in followers_id_list:
                id = following_user["id"]
                client.unfollow_user(target_user_id=id)
                print(f"remove: {id}")
                remove_count += 1
                time.sleep(SLEEP_SECOND)
    except Exception as e:
        print(e)


def main(client):
    exec_follow(client)
    exec_remove(client)


if __name__ == "__main__":
    client = get_client()
    main(client)

