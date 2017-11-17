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
    logger.debug("Refreshing all streams")
    for stream in settings.streams.all():
        if not refresh_stream(stream, settings):
            return False
    return True

def refresh_token(settings):
    # Request a new token
    url = API_TOKENS
    if not settings.refresh:
        logger.warn("No Refresh token available")
        return False
    logger.info("Refreshing Feedly access token")
    payload = {
        'refresh_token': settings.refresh,
        'client_id': 'feedlydev',
        'client_secret': 'feedlydev',
        'grant_type': 'refresh_token'
    }
    contents = requests.post(url, data=payload).json()
    if not 'access_token' in contents or not contents['access_token']:
        logger.warn("Access token could not be refreshed.")
        logger.debug(contents)
        return False
    settings.token = contents['access_token']
    settings.save()
    return True

def refresh_stream(stream, settings, retry=False):
    # Start a request to download the feed for a particular stream
    logger.info("Processing stream %s" % stream.title)
    url = API_STREAMS + stream.ident
    headers = { 'Authorization': 'OAuth ' + settings.token }
    contents = requests.get(url, headers=headers).json()
    if 'errorMessage' in contents:
        errmsg = contents['errorMessage']
        # Usually this is a token expired
        if 'expired' in errmsg or 'unauthorized' in errmsg:
            logger.debug(errmsg)
            if not refresh_token(settings): return False
            # Make another attempt
            if retry or not refresh_stream(stream, settings, True): return False
        else:
            # Otherwise log the issue
            logger.error(errmsg)
            return False
    if not 'items' in contents:
        logger.error("Could not obtain contents after retrying")
        logger.debug(contents)
        return False
    for raw_entry in contents['items']:
        eid = raw_entry['id']
        # Create or update data
        if Entry.objects.filter(entry_id=eid).exists():
            logger.info("Skipping entry '%s'" % eid)
        else:
            logger.info("Adding entry '%s'" % eid)
            entry = Entry()
            # Parse the Feedly object
            entry = feedparser.parse(entry, raw_entry, stream)
            # Persist resulting object
            entry.save()
    return True
