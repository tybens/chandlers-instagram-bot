import time
import argparse
import os

from decouple import config
from instagrapi import Client
from datetime import datetime
import wikipedia
from googlesearch import search

from utils.generate_photo import generate_photo, generate_photo_from_query
from utils.scrape import generate_posts_data_from_scrape_data, scrape_for_albums
from utils import read_comments_data, read_posts_data

def login(production=False) -> object:
    """ Uses instagrapi to get a logged-in client for ig api interaction """
    cl = Client()

    USERNAME = "chandlers_favorite_album"
    if production: 
        PASSWORD = os.environ.get("PASSWORD")
    else:
        PASSWORD = config("PASSWORD")
    NEW_DUMP = True  # change to True on first run of the day I think

    if NEW_DUMP:
        cl.login(USERNAME, PASSWORD)
        # cl.dump_settings('./dump.json')
    else:
        cl.load_settings("./dump.json")
        cl.login(USERNAME, PASSWORD)

    return cl


def photo_upload(cl, path, caption) -> bool:
    """ Uploads a photo to instagram """

    try:
        cl.photo_upload(path, caption)  # upload photo
        return True
    except Exception as e:
        print("error", e)
        return False


def main(cl, TOTAL_POSTS):
    """ The main posting functionality 

    Needs a csv with post data inside to be able to post
    """
    data = read_posts_data()
    try:
        start_index = data.date_posted.to_list().index("")
    except ValueError:
        print("all posts in posts.csv have been posted!")
        return

    posts = 0
    for index, post_data in data.iloc[start_index:].iterrows():
        username = post_data["username"]
        album = post_data["album"]
        artist = post_data["artist"]
        url = post_data["url"]

        # can only post 25 posts per 24 hours
        if posts > TOTAL_POSTS:
            break

        # generate the photo and caption
        path = generate_photo(url, username)
        # this caption kept getting me flagged for spamming
        # caption = f"{album} by {artist} as requested by {username} \n - \n @friends @mattyperry4 #friends #matthewperry #friendsmemes #chandlerbing #music #album #song #band #rock #country #electronic #pop #punk #rap #hiphop #musicalbum #musicmemes #memes #chandler{artist_nospace}"
        try:
            summary = wikipedia.summary(album + f" ({artist} album)", sentences=2)
        except:
            summary = ""
        thisSearch = search(artist + " Instagram")[0]
        handle = thisSearch.split("/")[-2] if "instagram" in thisSearch else ""
        artist_nospace = artist.replace(" ", "")
        caption = f"{album} by {artist} as requested by {username} \n - \n" + summary + \
            f" \n - \n@{handle} @friends #{artist_nospace} #photoshop #record #album #chandler{artist_nospace}"

        # if successful generation, upload it
        photo_upload(cl, path, caption)
        data.loc[index, "date_posted"] = str(datetime.now())
        posts += 1  # iterate posts
        print(f"{posts} uploaded album: {album} \t thanks to username: {username}")

        # wait 5 seconds
        time.sleep(5)

    # change account picture to be the most recent post
    try:
        cl.account_change_picture(path)
    except:
        pass

    # re-save the posts csv to have the date_posted on it
    data.to_csv("data/posts.csv")
    return


if __name__ == "__main__":
    """ actions: "scrape_posts", "scrape_comments", "post", "photoshop" """
    parser = argparse.ArgumentParser()
    parser.add_argument("--ACTION", "-a", type=str,
                        help="str of which action to do. 'p' for post, 'sp' for scrape posts, 'sc' for scrape comments, 'ps' for photoshop")
    args = parser.parse_args()
    action_mapper = {"p": "post", "sp": "scrape_posts",
                     "sc": "scrape_comments", "ps": "photoshop"}
    ACTION = action_mapper[args.ACTION]

    if ACTION == "scrape_posts":
        generate_posts_data_from_scrape_data()
    elif ACTION == "scrape_comments":
        cl = login()  # login
        mediaIds = [media.id for media in cl.user_medias(cl.user_id_from_username('chandler_holding_ur_fav_album'), 1000)]
      
        for ID in mediaIds:
            scrape_for_albums(cl, ID)
    elif ACTION == "post":
        TOTAL_POSTS = 4 # max 25 I think
        cl = login()  # login
        main(cl, TOTAL_POSTS)
    elif ACTION == "photoshop":
        username = "@test"
        query = "lausse the cat"
        generate_photo_from_query(query, username)
