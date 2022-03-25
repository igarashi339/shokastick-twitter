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


def is_theater_account(name:str, description:str):
    """
    当該ユーザが演劇のアカウントかどうか判定する。
    """
    target_word_list = ["演劇", "劇団", "俳優", "舞台", "芝居", "役者", "主宰", "シナリオライター", "インプロ"]
    for target_word in target_word_list:
        if target_word in name:
            return True
        if target_word in description:
            return True
    return False


def get_follow_back_rate(user_id):
    """
    当該ユーザのフォローバック率を求める。
    """
    pass


def get_promising_follower(client, user_id):
    """
    対象ユーザのフォロワー(最初の1000人)のうち、フォローバックしてくれそうな人を返す。
    """
    target_user_list = []
    followers = client.get_users_followers(user_id, max_results=1000, user_fields="protected,public_metrics,description")
    for follower in followers.data:
        id = follower["id"]
        username = follower["username"]
        name = follower["name"].replace(",", "、")
        following_count = follower["public_metrics"]["following_count"]
        followers_count = follower["public_metrics"]["followers_count"]
        description = follower["description"]
        following_follower_rate = float(following_count) / float(followers_count) if followers_count != 0 else 100

        # 鍵アカは候補から外す
        if follower["protected"]:
            continue
        # following, followerの少ない人は候補から外す
        if following_count <= 10 or followers_count <= 10:
            continue
        # following/follower高すぎる、低すぎる人は候補から外す
        if following_follower_rate < 0.5 or following_follower_rate > 2:
            continue
        # 演劇のアカウントでなければ候補から外す
        if not is_theater_account(name, description):
            continue
        target_user_list.append([id, username, name])
    return target_user_list


def main():
    client = get_client()
    target_user_list = get_promising_follower(client, "957073448487944192")
    with open("target_users.csv", "a", encoding="utf-8") as f:
        for target_user in target_user_list:
            f.write(f"{target_user[0]},{target_user[1]},{target_user[2]}\n")


if __name__ == "__main__":
    main()

