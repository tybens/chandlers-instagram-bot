import requests
import re
import io
import random
import string

from bs4 import BeautifulSoup
from PIL import Image

COORDS =[(93, 204), (303, 216), (31, 354), (250, 405)]

COEFFS = [ 7.87970803e-01,  3.25694599e-01, -5.58891931e+02, -5.62940129e-02,
        9.85145226e-01, -7.82937132e+02,  3.63585476e-04,  3.74690231e-04] 


def download_image(url):
    """Download a PIL image from a url"""
    return Image.open(io.BytesIO(requests.get(url).content)).convert(mode='RGBA')


def generate_photo(album_url, username) -> str:
    """ Generates the chandler album photo from the specific album url """

    # 'images/*' won't work when running as python command because of different pwd
    bg = Image.open('./images/large/chandler.png').convert(mode='RGBA')
    fg = Image.open('./images/large/chandler_front.png').convert(mode='RGBA')

    album = download_image(album_url).resize((bg.width, bg.height), resample=Image.ANTIALIAS)
    # commented out to make chandler hold the placeholder
    # album = Image.open('../../public/images/placeholder.png').convert(mode='RGBA')
    
    width, height = 384, 384
    album = album.resize((width, height), resample=Image.ANTIALIAS)
    coeffs = COEFFS
    # coeffs = find_coeffs(
    #     [(0, 0), (width, 0), (0, height), (width, height)], scale(COORDS[idx], factor=4)
    # )
    album = album.transform((width * 4, height * 4), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    album = album.resize((bg.width, bg.height), resample=Image.ANTIALIAS)
    bg = Image.alpha_composite(bg, album)

    bg = Image.alpha_composite(bg, fg).convert("RGB")
    output = io.BytesIO()
    output.seek(0)

    token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    path = f"generated/{token}.jpg"
    bg.save(path, format='jpeg')

    return path


def search(query):
    resp = requests.get(f'https://www.last.fm/search/albums?q={query}')
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "lxml")

    return [
        {
            'url': re.sub(r'(\d+s)', '100s',
                          x.find('img').attrs['src']),
            'album': x.find('h4').a.text,
            'artist': x.find('p').a.text,
        } for x in soup.findAll('div', {'class': 'album-result-inner'})
    ]

def generate_photo_from_query(album_query, username):
    """ generates a jpeg file in `images/{username}.jpg` from the first result of the album query """

    # get the album data from the search query
    data = search(album_query)

    # if the query failed, return false
    if len(data) == 0:
        return False, "", ""


    # generate the photo
    path = generate_photo(data[0]["url"], username)

    return True, path, data[0]["album"]

if __name__ == '__main__':
    # print(search('city of the weak'))
    username = "ptvogtman"
    test_url = 'https://lastfm.freetls.fastly.net/i/u/300x300/86b35c4eb3c479da49c915d8771bbd1a.png'
    # generate_photo(test_url, username)

    test_query = "to pimp a butterfly"

    generate_photo_from_query(test_query, username)