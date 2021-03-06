from csv import DictReader
import pandas as pd


def read_comments_data():
    """ Reads comments data """
    df = pd.read_csv("data/comments.csv")
    
    return df


def read_posts_data():
    """ Reads posts.csv and returns a pandas.DataFrame """
    df = pd.read_csv("data/posts.csv", index_col=0)
    df["date_posted"] = df["date_posted"].fillna("")
    
    return df


def clean_posts_data(df):
    """ Cleans dataframe of posts data and throws into data/posts.csv """

    df["username"] = df["username"].apply(lambda x: "@"+x if "@" not in x else x)  # add @ symbol
    # group usernames into list of usernames
    df_new = df.groupby(["url"]).agg({"username": lambda x: ", ".join(set(
        x)), "album": "first", "artist": "first", "date_posted": "first", "url": "first"}).reset_index(drop=True)
    # so that we don't have duplicated urls that have already been posted
    df_new.drop_duplicates(subset=["url"], keep="first")
    df_new = df_new.sort_values("date_posted", ascending=True).reset_index(drop=True)
    df_new['username'] = df_new.username.apply(lambda x: ', '.join(set(x.split(', '))))
    df_new.to_csv("data/posts.csv")  # write data

def change_caption(cl, post_url, new_caption):
    media_pk = cl.media_pk_from_url(post_url)
    cl.media_edit(media_pk, new_caption)