#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass
from gmusicapi import Mobileclient

import setlistfm

def login():
    """Make an instance of the api and attempts to login with it.
    Return the authenticated api.
    """

    # We're not going to upload anything, so the Mobileclient is what we want.
    api = Mobileclient()

    logged_in = False
    attempts = 0

    while not logged_in and attempts < 3:
        email = raw_input('Email: ')
        password = getpass()

        logged_in = api.login(email, password, Mobileclient.FROM_MAC_ADDRESS)
        attempts += 1

    return api

def make_setlist(band_name):
    setlist = []

    for song in setlistfm.get_setlist(band_name):
         setlist.append(api.search(band_name + " " + song)['song_hits'][0]['track']['nid'])   
    
    return setlist

def make_playlist():
    api = login()

    if not api.is_authenticated():
        print "Sorry, those credentials weren't accepted."
        return

    print 'Successfully logged in.'
    print

    band_name = raw_input('Enter band name: ')

    playlist_name = band_name + " Setlist"
    playlist_id = api.create_playlist(playlist_name)

    print 'Created playlist.'
    print

    setlist = make_setlist(band_name)

    api.add_songs_to_playlist(playlist_id, setlist)

    print 'Added songs to playlist!!'
    print

    api.logout()
    
    print 'Logged out. Goodbye'

if __name__ == '__main__':
    make_playlist()
