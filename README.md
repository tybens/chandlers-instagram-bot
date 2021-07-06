# Chandlers Instagram Bot

Scrapes [@chandler_holding_ur_fav_album](https://www.instagram.com/chandler_holding_ur_fav_album/) for album requests, photoshops chandler to be holding the album, and posts the photo to [@chandlers_favorite_album](https://www.instagram.com/chandlers_favorite_album/) instagram page. 

Some of this code is adopted from my other repo [chandlers-favorite-album](https://github.com/tybens/chandlers-favorite-album) which makes the website [chandlersfavoritealbum.com](https://chandlersfavoritealbum.com/)


#### Example command:

Post bot post. Chandler instagram bot will post 24 posts found in `data/posts.csv` as long as they don't have a `date_posted` data point

```Bash
python bot.py -a=p
```