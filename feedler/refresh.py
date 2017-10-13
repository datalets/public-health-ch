# -*- coding: utf-8 -*-

import requests, json, codecs

import logging
logger = logging.getLogger('feedler')

from .models import Entry
from feedler import feedparser

API_BASEURL = 'https://cloud.feedly.com/v3/'
API_STREAMS = API_BASEURL + 'streams/contents?streamId='
API_TOKENS = API_BASEURL + 'auth/token'

def refresh_streams(settings):
    # Iterate through all saved streams
    logger.warn("Refreshing all streams")
    for stream in settings.streams.all():
        if not refresh_stream(stream, settings):
            return False
    return True

def get_headers(settings):
    return {
        'Authorization': 'OAuth ' + settings.token
    }

def refresh_token(settings):
    # Request a new token
    url = API_TOKENS
    logger.warn("Refreshing Feedly access token")
    payload = {
        'refresh_token': settings.token,
        'client_id': 'feedlydev',
        'client_secret': 'feedlydev',
        'grant_type': 'refresh_token'
    }
    contents = requests.get(url, data=payload, headers=get_headers(settings)).json()
    if not 'access_token' in contents or not contents['access_token']:
        logger.error("Access token could not be refreshed.")
        return False
    settings.token = contents['access_token']
    settings.save()
    return True

def refresh_stream(stream, settings, retry=False):
    # Start a request to download the feed for a particular stream
    logger.warn("Processing stream %s" % stream.title)
    url = API_STREAMS + stream.ident
    contents = requests.get(url, headers=get_headers(settings)).json()
    if 'errorMessage' in contents:
        # Usually this is a token expired
        if 'token expired' in contents['errorMessage'] or 'unauthorized' in contents['errorMessage']:
            if not refresh_token(settings): return False
            # Make another attempt
            if retry or not refresh_stream(stream, settings, True):
                return False
        else:
            logger.error(contents['errorMessage'])
            return False
    for raw_entry in contents['items']:
        eid = raw_entry['id']
        # Create or update data
        try:
            entry = Entry.objects.get(entry_id=eid)
            logger.info("Updating entry '%s'" % eid)
        except Entry.DoesNotExist:
            logger.info("Adding entry '%s'" % eid)
            entry = Entry()
        # Parse the Feedly object
        entry = feedparser.parse(entry, raw_entry, stream)
        # Persist resulting object
        entry.save()
