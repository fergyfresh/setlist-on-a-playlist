#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass

from gmusicapi import Mobileclient
import setlistfm

def ask_for_credentials():
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


def demonstrate():
    """Demonstrate some api features."""

    api = ask_for_credentials()

    if not api.is_authenticated():
        print "Sorry, those credentials weren't accepted."
        return

    print 'Successfully logged in.'
    print

    # Get all of the users songs.
    # library is a big list of dictionaries, each of which contains a single song.
    print 'Loading library...',
    library = api.get_all_songs()
    print 'done.'

    band_name = raw_input('Enter band name: ')

    setlist_song_ids = {}
    
    for song in setlistfm.get_setlist(band_name):
        setlist_song_ids[song] = '1'
   
    for song in library:
        try:
            if setlist_song_ids[song['title']] == '1':
                setlist_song_ids[song['title']] = song['id']
        except:
            pass

    print "I'm going to make a new playlist and add the songs from"
    print "the setlist to is."
    print
    playlist_name = band_name + "'s Last Setlist"

    # Like songs, playlists have unique ids.
    # Google Music allows more than one playlist of the samQe name;
    # these ids are necessary.
    playlist_id = api.create_playlist(playlist_name)
    print 'Made the playlist.'
    print

    # Now let's add the song to the playlist, using their ids:
    api.add_songs_to_playlist(playlist_id, setlist_song_ids.values())
    print 'Added the song to the playlist.'
    print

    # We're all done! The user can now go and see that the playlist 
    #is there. The web client syncs our changes in real time.
    delete_me = raw_input('You can now check on Google Music that \
          the playlist exists. When done, type delete if you want \
          to delete the playlist:')

    if delete_me == 'delete':
        api.delete_playlist(playlist_id)
        print 'Deleted the playlist.'

    # It's good practice to logout when finished.
    api.logout()
    print 'All done!'

if __name__ == '__main__':
    demonstrate()
