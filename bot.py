import time

from decouple import config
from instagrapi import Client
from datetime import datetime

from utils.generate_photo import generate_photo
from utils.scrape import generate_posts_data_from_scrape_data, scrape_for_albums
from utils import read_scrape_data, read_posts_data


def login() -> object:

    cl = Client()

    USERNAME = "chandlers_favorite_album"
    PASSWORD = config("PASSWORD")
    NEW_DUMP = False  # change to True on first run of the day I think

    if NEW_DUMP:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings('./dump.json')
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


def main(cl):

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
        if posts > 24:
            break

        # generate the photo and caption
        path = generate_photo(url, username)
        artist_nospace = artist.replace(" ", "")
        # this caption kept getting me flagged for spamming 
        # caption = f"{album} by {artist} as requested by {username} \n - \n @friends @mattyperry4 #friends #matthewperry #friendsmemes #chandlerbing #music #album #song #band #rock #country #electronic #pop #punk #rap #hiphop #musicalbum #musicmemes #memes #chandler{artist_nospace}"
        caption = f"{album} by {artist} as requested by {username}"
       
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
    # actions: "scrape_posts", "scrape_comments", "post"
    ACTION = "post"

    cl = login()  # login

    if ACTION == "scrape_posts":
        generate_posts_data_from_scrape_data()
    elif ACTION == "scrape_comments":
        POST_URL = "https://www.instagram.com/p/CEmZFT0lzxk/"
        scrape_for_albums(cl, POST_URL)
    elif ACTION == "post":
        main(cl)
