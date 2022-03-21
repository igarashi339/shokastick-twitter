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


def get_client():
    return tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)


def exec_follow(client):
    data_num = 3
    try:
        result = urllib.request.urlopen(gas_url + f"?datanum={data_num}")
        user_info_list = json.loads(result.read())
    except Exception as e:
        print(e)
    for user_info in user_info_list:
        client.follow_user(target_user_id=user_info["id"])
        time.sleep(10)


def exec_remove(client):
    pass


def main(client):
    exec_follow(client)
    exec_remove(client)


if __name__ == "__main__":
    client = get_client()
    main(client)

