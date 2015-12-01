import requests
from BeautifulSoup import BeautifulSoup

URL = 'http://www.setlist.fm/search?query='
band_name = 'the+smith+street+band'
r = request.get(URL+band_name)

soup = BeatifulSoup(r.text)

for link in soup.findAll('a'):
     print(link.get('href'))

