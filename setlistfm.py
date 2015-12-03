import requests
from BeautifulSoup import BeautifulSoup

def make_band_showlist_url (band_name):
    return 'http://www.setlist.fm/search?query=' \
	   + "+".join(band_name.split())

def find_newest_setlist_link (url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)    
    for a_tag in soup.findAll('a'):
	link = a_tag.get('href')
	try:
    	    if a_tag.get('href').find('setlist/') == 0:
        	setlist_link = link
        	break	 
	except:
            pass
    return 'http://www.setlist.fm/' + setlist_link

def get_setlist (band_name):
    band_url = make_band_showlist_url(band_name)
    newest_setlist = find_newest_setlist_link(band_url)
    r = requests.get(newest_setlist)
    soup = BeautifulSoup(r.text)
    songlinks = soup.findAll("a", {"class":"songLabel"})
    songlist = [song_link.string for song_link in songlinks]
    return songlist

test = get_setlist('the smith street band')
    
