# Chandlers Instagram Bot

Scrapes [@chandler_holding_ur_fav_album](https://www.instagram.com/chandler_holding_ur_fav_album/) for album requests, photoshops chandler to be holding the album, and posts the photo to [@chandlers_favorite_album](https://www.instagram.com/chandlers_favorite_album/) instagram page. 

Some of this code is adopted from my other repo [chandlers-favorite-album](https://github.com/tybens/chandlers-favorite-album) which makes the website [chandlersfavoritealbum.com](https://chandlersfavoritealbum.com/)


#### Example command:

Bot will post. Chandler instagram bot will post 24 posts found in `data/posts.csv` as long as they don't have a `date_posted` data point

```Bash
python bot.py -a=p
```

#### To deploy to aws lambda

This zips the contents to `../zipfile.zip`. Which can be uploaded to an aws lambda instance.

```Bash
serverless # initializes as a serverless repo
sls plugin install -n serverless-python-requirements # lets me bundle the python requirements
sls deploy
```

##### useful links
- https://www.serverless.com/framework/docs/providers/aws/guide/credentials/
- https://www.serverless.com/plugins/serverless-python-requirements
- https://stackoverflow.com/questions/53824556/how-to-install-numpy-and-pandas-for-aws-lambdas
- 
