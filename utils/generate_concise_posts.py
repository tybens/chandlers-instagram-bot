import pandas as pd
import numpy as np
from datetime import datetime
import wikipedia
from googlesearch import search
import json
from bot import login
from utils import change_caption
from utils.generate_photo import generate_photo, generate_photo_from_query
from utils.scrape import generate_posts_data_from_scrape_data, scrape_for_albums
from utils import read_comments_data, read_posts_data


def generate_concise_posts():
    data = []
    posts = 0
    df = pd.read_csv("data/posts.csv", index_col=0)
    df.date_posted.fillna("_", inplace=True)

    for _, post_data in df.iterrows():
        posts += 1
        username = post_data["username"]
        album = post_data["album"]
        artist = post_data["artist"]
        url = post_data["url"]
        date_posted = post_data["date_posted"]

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
            f" \n - \n@{handle} @friends #{artist_nospace} #photoshop #record #album #chandlerholdingurfavalbum #chandler{artist_nospace}"

        data.append({"caption": caption, "path_to_pic": path, "artist_handle": handle, "date_posted": date_posted })
        print(f"{posts} generated album: {album} \t thanks to username: {username}\t date: {date_posted}\t path: {path}")


    new_df = pd.DataFrame(data)

    new_df.to_csv("data/concise_posts.csv")

    # convert to json and save to file
    tmp = new_df.to_dict(orient="records")
    textfile = open("data/posts_concise.json", "w")
    a = textfile.write("{'posts': "+json.dumps(tmp)+"}")
    textfile.close()
