# Chandlers Instagram Bot

Scrapes [@chandler_holding_ur_fav_album](https://www.instagram.com/chandler_holding_ur_fav_album/) for album requests, photoshops chandler to be holding the album, and posts the photo to [@chandlers_favorite_album](https://www.instagram.com/chandlers_favorite_album/) instagram page.

Some of this code is adopted from my other repo [chandlers-favorite-album](https://github.com/tybens/chandlers-favorite-album) which makes the website [chandlersfavoritealbum.com](https://chandlersfavoritealbum.com/)

#### Example command:

Bot will post. Chandler instagram bot will post 24 posts found in `data/posts.csv` as long as they don't have a `date_posted` data point

```Bash
python bot.py -a=p
```

### To deploy to google cloud platform to run the script daily

#### !! Data stored in `data/` is outdated and is now hosted on chandlers-instagram-bot firebase realtime database

Uses gcloud command line. This deploys the function to google cloud functions, set to trigger on the trigger topic DAILY_POSTS.

```Bash
gcloud functions deploy post_to_insta --trigger-topic DAILY_POSTS --runtime python39 --allow-unauthenticated
```

Creates pubsub trigger topic DAILY_POSTS.

```Bash
gcloud pubsub topics create DAILY_POSTS
```

Go into google console to create a Cloud Scheduler job that triggers the function daily.

##### useful links

- https://cloud.google.com/functions/docs/writing/background
- https://cloud.google.com/functions/docs/calling/pubsub
- https://cloud.google.com/functions/docs/quickstart-python
- https://www.cloudsavvyit.com/4975/how-to-run-gcp-cloud-functions-periodically-with-cloud-scheduler/
