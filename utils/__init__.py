from csv import DictReader
import pandas as pd


def read_scrape_data():
    """ Reads scrape data """
    with open('data/comments.csv', 'r') as read_obj:  # read csv file as a list of lists
        # pass the file object to reader() to get the reader object
        dict_reader = DictReader(read_obj)
        data = list(dict_reader)
    return data


def read_posts_data():
    """ Reads posts.csv and returns a pandas.DataFrame """
    df = pd.read_csv("data/posts.csv", index_col=0)
    df["date_posted"] = df["date_posted"].fillna("")
    
    return df


def clean_posts_data():
    filename = "data/posts.csv"
    df = pd.read_csv(filename, header=0)  # read data
    df["username"] = df["username"].apply(lambda x: "@"+x)  # add @ symbol
    # change NaNs to empty strings
    df["date_posted"] = df["date_posted"].fillna("")
    df_new = df.groupby(["url"]).agg({"username": lambda x: ", ".join(set(
        x)), "album": "first", "artist": "first", "date_posted": "first", "url": "first"}).reset_index(drop=True)
    # so that we don't have duplicated urls that have already been posted
    df_new.drop_duplicates(subset=["url"], keep="first")
    df_new.to_csv("data/posts.csv")  # write data
