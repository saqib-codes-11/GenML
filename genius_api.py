# https://docs.genius.com/

# import requests
import urllib2
import json
import pandas
import unicodedata
# import time
from datetime import date

AUTH_TOKEN = "4OJhKq4UxyXPDNw9BM9BxvLwHtdGxcmwTtPzv_toigTps1vaVvbYow8cg-v0A5z4"
_URL_API = "https://api.genius.com/"

artists = ["2Pac", "Eminem", "Ice Cube", "Outkast", "Nas", "DMX",
           "The Game", "T.I.", "Kanye West", "Kendrick Lamar"]

data = {
    'Artist': [],
    'Genius_IQ': [],
    'Followers': [],
    'Is_Verified': [],
    'Meme_Verified': [],
    'Song_Title': [],
    'Annotation_Count': [],
    'Release_Date': [],
    'Featured_Video': [],
    'Hot': [],
    'Accepted_Annotations': [],
    'Number_Contributors': [],
    'Number_Verified_Annotations': [],
    'Page_Views': [],
    'Pyong_Count': [],
    'Classification': [],
    'Referent_ID': [],
    'Length_Referent_Text': [],
    'Is_Description': [],
    'Total_Votes': [],
    'Pinned': [],
    'Comment_Count': [],
    'Annotation_Is_Verified': []
}


def genius_search(term):
    """Search genius, given a string. Search can return anything"""
    _URL_SEARCH = "search?q="
    querystring = _URL_API + _URL_SEARCH + urllib2.quote(term)
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + AUTH_TOKEN)
    request.add_header("User-Agent", "")

    response = urllib2.urlopen(request, timeout=10)
    raw = response.read()
    json_obj = json.loads(raw)
    return json_obj


def get_artist(artist):
    """Returns an artist object given a search term"""
    songres = genius_search(artist)
    # hits = songres['response']['hits']
    if len(songres['response']['hits']) == 0:
        print 'There were no artists that matched the search'
        return -1
    else:
        artist_id = songres['response']['hits'][0]['result']['primary_artist']['id']
        _URL_ARTIST = "artists/{}".format(artist_id)
        querystring = _URL_API + _URL_ARTIST
        request = urllib2.Request(querystring)
        request.add_header("Authorization", "Bearer " + AUTH_TOKEN)
        request.add_header("User-Agent", "")

        response = urllib2.urlopen(request, timeout=10)
        raw = response.read()
        json_obj = json.loads(raw)
        return json_obj['response']['artist']


def get_artist_songs(artist_id, num):
    """ Get song objects for an artist given an artists ID"""
    _URL_SONGS = "artists/{}/songs?sort=popularity&per_page={}".format(artist_id, str(num))
    querystring = _URL_API + _URL_SONGS
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + AUTH_TOKEN)
    request.add_header("User-Agent", "")

    response = urllib2.urlopen(request, timeout=10)
    raw = response.read()
    json_obj = json.loads(raw)
    return json_obj['response']['songs']


def get_song_info(song_id):
    _URL_SONG = "songs/{}".format(song_id)
    querystring = _URL_API + _URL_SONG
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + AUTH_TOKEN)
    request.add_header("User-Agent", "")

    response = urllib2.urlopen(request, timeout=10)
    raw = response.read()
    json_obj = json.loads(raw)
    return json_obj['response']['song']


def get_referents(song_id):
    """ Get referent objects for a song given a song's ID"""
    _URL_REFERENTS = "referents?song_id={}".format(song_id)
    querystring = _URL_API + _URL_REFERENTS
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + AUTH_TOKEN)
    request.add_header("User-Agent", "")

    response = urllib2.urlopen(request, timeout=10)
    raw = response.read()
    json_obj = json.loads(raw)
    return json_obj['response']['referents']


def get_data(key, obj):
    # Make sure that the key exists in the object
    if key in obj:
            data = obj[key]
            if data is None:
                return '?'
    else:
        data = '?'

    return data


def get_days(release):
    # print release
    if release is None or release == '?':
        return '?'
    else:
        today = date.today()
        year, month, day = release.split('-')
        release_date = date(int(year), int(month), int(day))
        time_from_release = abs(release_date - today)
        return time_from_release.days
    return '?'

def add_data(header, info):
    data[header].append(info)


def writet_to_csv(data):
    df = pandas.DataFrame(data)
    df.to_csv('./data.csv')


# Where we collect the data!
if __name__ == '__main__':

    for artist in artists:
        art_obj = get_artist(artist)

        if art_obj == -1:
            continue

        art_id = get_data('id', art_obj)
        art_iq = get_data('iq', art_obj)
        art_followers = get_data('followers_count', art_obj)
        art_verified = get_data('is_verified', art_obj)
        art_meme_verified = get_data('is_meme_verified', art_obj)

        art_songs = get_artist_songs(art_id, 30)

        print artist

        for art_song in art_songs:
            print "   ."
            song_id = get_data('id', art_song)
            song = get_song_info(song_id)

            song_title = unicodedata.normalize('NFKD', get_data('full_title', song)).encode('ascii', 'ignore')
            annotation_count = get_data('annotation_count', song)
            release_date = get_days(get_data('release_date', song))
            featured_video = get_data('featured_video', song)
            stats = get_data('stats', song)
            hot = get_data('hot', stats)
            accepted_annotations = get_data('accepted_annotations', stats)
            number_contributors = get_data('contributors', stats)
            number_verified_annotations = get_data('verified_annotations', stats)
            page_views = get_data('pageviews', stats)
            pyong_count = get_data('pyongs_count', song)

            song_refs = get_referents(song_id)

            for referent in song_refs:

                referent_id = get_data('id', referent)
                length_referent_text = len(get_data('content', get_data('range', referent)))  # length of the text to which the referent is referring. The length of that actual annotation you can get below from annotation
                is_description = get_data('is_description', referent)
                classification = get_data('classification', referent)

                for annotation in referent['annotations']:

                    total_votes = get_data('votes_total', annotation)
                    pinned = get_data('pinned', annotation)
                    comment_count = get_data('comment_count', annotation)
                    annotation_is_verified = get_data('verified', annotation)

                    # Adding the data to our data dictionary
                    add_data('Artist', artist)
                    add_data('Genius_IQ', art_iq)
                    add_data('Followers', art_followers)
                    add_data('Is_Verified', art_verified)
                    add_data('Meme_Verified', art_meme_verified)
                    add_data('Song_Title', song_title)
                    add_data('Annotation_Count', annotation_count)
                    add_data('Release_Date', release_date)
                    add_data('Featured_Video', featured_video)
                    add_data('Hot', hot)
                    add_data('Accepted_Annotations', accepted_annotations)
                    add_data('Number_Contributors', number_contributors)
                    add_data('Number_Verified_Annotations', number_verified_annotations)
                    add_data('Page_Views', page_views)
                    add_data('Pyong_Count', pyong_count)
                    add_data('Classification', classification)
                    add_data('Referent_ID', referent_id)
                    add_data('Length_Referent_Text', length_referent_text)
                    add_data('Is_Description', is_description)
                    add_data('Total_Votes', total_votes)
                    add_data('Pinned', pinned)
                    add_data('Comment_Count', comment_count)
                    add_data('Annotation_Is_Verified', annotation_is_verified)

    # print json.dumps(data, indent=4, sort_keys=True)
    writet_to_csv(data)
