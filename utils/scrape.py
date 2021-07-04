import csv
import re

from . import read_scrape_data, clean_posts_data
from .generate_photo import search

def scrape_for_albums(cl, post_url):
    """ Scrapes a chandler_holding_ur_fav_album post_id for people requesting albums """
    # data = [
    #     {
    #         "album_query": "to pimp a butterfly",
    #         "username": "ptvogtman"
    #     }
    # ]

    file = open("data/comments.csv", "w+")
    writer = csv.writer(file)
    writer.writerow(["username", "query"])

    media_id = cl.media_id(cl.media_pk_from_url(post_url))
    comments = cl.media_comments(media_id)

    for comment in comments:
        query = filter_for_query(comment.text)
        if query:
            writer.writerow([comment.user.username, query])

    return 

def filter_for_query(text):
    checks = ["by", "-"]
    ret = ""
    for check in checks:
        if check in text and ret == "":
            try:
                split = text.split(" ")
                index = split.index(check)
                ret = " ".join([split[index-1].lower() if split[index-1].lower() != "album" else split[index-2].lower(), split[index+1].lower()])
            except:
                continue
    ret = re.sub(r'\W', '', ret) # replace special characters with nothing
    return ret

def generate_posts_data_from_scrape_data():
    """ generates a jpeg file in `images/{username}.jpg` from the first result of the album query """

    file = open("data/posts.csv", "a+")
    writer = csv.writer(file)
    writer.writerow(["username", "album", "url", "artist", "date_posted"])

    # read scrape data
    scrape_data = read_scrape_data()

    for row in scrape_data:
        # search the query
        data = search(row["query"])
        # if the query returned data
        if len(data) != 0:
            # write all the info we need for a post to a csv file
            writer.writerow([row["username"], data[0]["album"], data[0]["url"], data[0]["artist"], ""])
    
    # clean the posts data
    clean_posts_data()

    return

if __name__ == "__main__":
    from bot import login

    POST_URL = "https://www.instagram.com/p/CEmZFT0lzxk/"
    cl = login()

    print("logged in...")

    # scrape_for_albums(cl, POST_URL)

    generate_posts_data_from_scrape_data()




