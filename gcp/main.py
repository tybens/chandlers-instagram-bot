import os

from datetime import datetime
# from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, db
from instagrapi import Client
from instagrapi.types import Usertag

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./service_account_key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chandlers-instagram-bot-default-rtdb.firebaseio.com/',
})


def post_to_insta(event=None, context=None):
    # instagram client
    cl = login()

    # get the reference to the first 4 posts that haven't been posted
    ref = db.reference('posts')
    snapshot = ref.order_by_child('date_posted').equal_to(
        '_').limit_to_first(3).get()

    # iterate through and post them and update data point
    i = 0
    for key, val in snapshot.items():
        i += 1
        print('{0} => {1}'.format(key, val))

        usertags = [Usertag(user=cl.user_info_by_username(
            val['artist_handle']), x=0.45, y=0.72)]
        cl.photo_upload(val['path_to_pic'], val['caption'], usertags=usertags)

        # update date posted to now
        ref.child(key).update({'date_posted': str(datetime.now())})

        if i == 3: cl.account_change_picture(val['path_to_pic'])

    return f'Success'


def login(production=False) -> object:
    """ Uses instagrapi to get a logged-in client for ig api interaction """
    cl = Client()

    USERNAME = "chandlers_favorite_album"
    PASSWORD = os.environ.get("INSTA_PASSWORD")

    cl.login(USERNAME, PASSWORD)

    return cl


if __name__ == "__main__":
    post_to_insta()
    # gcloud functions deploy post_to_insta --trigger-topic DAILY_POSTS --runtime python39 --allow-unauthenticated
