import tweepy
import time

consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

friends_ids = api.get_friend_ids()
followers_ids = api.get_follower_ids()

not_following_back = set(friends_ids) - set(followers_ids)

count = 0

for user_id in not_following_back:
    if count >= 40:
        print("Límite de usuarios alcanzado. Pausa de 1 hora...")
        time.sleep(3600)
        count = 0
    api.destroy_friendship(user_id=user_id)
    print(f"Dejaste de seguir al usuario con ID: {user_id}")
    count += 1