import csv

def scrape_for_albums(cl, post_url, writer):
    """ Scrapes a chandler_holding_ur_fav_album post_id for people requesting albums """
    # data = [
    #     {
    #         "album_query": "to pimp a butterfly",
    #         "username": "ptvogtman"
    #     }
    # ]

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
                ret = " ".join([split[index-1].lower() if split[index-1].lower() != "album" else split[index-2], split[index+1]])
            except:
                continue
    
    return ret


if __name__ == "__main__":
    from bot import login

    POST_URL = "https://www.instagram.com/p/CEmZFT0lzxk/"
    cl = login()

    print(cl)
    print("logged in...")

    file = open("comments.csv", "w+")
    writer = csv.writer(file)
    writer.writerow(["username", "query"])

    scrape_for_albums(cl, POST_URL, writer)





