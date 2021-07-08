import csv
import re

import pandas as pd
import numpy as np

from . import read_comments_data, clean_posts_data
from .generate_photo import search


def scrape_for_albums(cl, media_id):
    """ Scrapes a chandler_holding_ur_fav_album post_id for people requesting albums """
    # data = [
    #     {
    #         "album_query": "to pimp a butterfly",
    #         "username": "ptvogtman"
    #     }
    # ]

    df = pd.read_csv("data/comments.csv")
    try:
        comments = cl.media_comments(media_id)
    except:
        comments = []
        
    for comment in comments:
        query = filter_for_query(comment.text)
        if query:
            df = df.append({'username': comment.user.username, 'query': query}, ignore_index=True)

    df.to_csv("data/comments.csv", index=False)
    return


def filter_for_query(text):
    checks = ["by", "-"]
    ret = ""
    for check in checks:
        if check in text and ret == "":
            try:
                split = text.split(" ")
                index = split.index(check)
                ret = " ".join([split[index-1].lower() if split[index-1].lower()
                               != "album" else split[index-2].lower(), split[index+1].lower()])
            except:
                continue
    # replace special characters with nothing
    ret = re.sub(r'[^a-zA-Z0-9\s]', '', ret)
    return ret


def generate_posts_data_from_scrape_data():
    """ generates a jpeg file in `images/{username}.jpg` from the first result of the album query """

    df = pd.read_csv("data/posts.csv", index_col=0)
    # writer.writerow(["username", "album", "url", "artist", "date_posted"])

    # read scrape data
    scrape_data = read_comments_data()

    for _, row in scrape_data.iterrows():
        # search the query
        data = search(row.query)
        # if the query returned data
        if len(data) != 0:
            # write all the info we need for a post to a csv file
            df = df.append({"username": "@"+row.username, "album": data[0]["album"], "artist": data[0]["artist"], "date_posted": np.NaN,
                           "url": data[0]["url"]}, ignore_index=True)


    # clean the posts data
    clean_posts_data(df)

    return


if __name__ == "__main__":
    from bot import login

    POST_URL = "https://www.instagram.com/p/CEmZFT0lzxk/"
    cl = login()

    print("logged in...")

    # scrape_for_albums(cl, POST_URL)

    generate_posts_data_from_scrape_data()
