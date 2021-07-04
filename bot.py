import time
import csv
from csv import DictReader

from decouple import config
from instagrapi import Client

from utils.generate_photo import generate_photo_from_query

def login() -> object:

    cl = Client()

    USERNAME = "chandlers_favorite_album"
    PASSWORD = config("PASSWORD")
    NEW_DUMP = False # change to True on first run of the day I think

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
        cl.photo_upload(path, caption) # upload photo
        return True
    except Exception as e:
        print("error", e)
        return False


def main():
    cl = login() # login

    data = read_scrape_data()

    for i, photo_data in enumerate(data):
        username = photo_data["username"]
        album_query = photo_data["album_query"]

        # can only post 25 posts per 24 hours
        if i > 24:
            return
        
        # generate the photo 
        success, path, album_name = generate_photo_from_query(album_query, username)
        
        if success:
            # generate caption
            caption = f"{album_name} requested by @{username}"

            # if successful generation, upload it
            if success: photo_upload(cl, path, caption)
            print(f"{i} uploaded query: {album_query} \t thanks to username: {username}")
            time.sleep(5) # wait 5 seconds

    cl.account_change_picture(path)

def read_scrape_data():
    with open('comments.csv', 'r') as read_obj: # read csv file as a list of lists
        dict_reader = DictReader(read_obj) # pass the file object to reader() to get the reader object
        data = list(dict_reader)
    return data

if __name__ == "__main__":
    main()
