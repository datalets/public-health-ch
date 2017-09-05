# -*- coding: utf-8 -*-

from datetime import datetime
from guess_language import guess_language

def parse(obj, raw, stream):
    """
    Parse raw JSON implementation from the Feedly API
    """
    obj.raw = raw
    obj.stream = stream
    obj.entry_id = raw['id']

    # Date stamp handling
    ts = raw['published'] / 1000
    obj.published = datetime.fromtimestamp(ts)

    # Authorship and title
    obj.title = raw['title']
    if 'author' in raw['origin']:
        obj.author = raw['author']
    elif 'title' in raw['origin']:
        obj.author = raw['origin']['title']

    # Parse links and references
    if len(raw['alternate']) > 0:
        obj.link = raw['alternate'][0]['href']
    if 'thumbnail' in raw and len(raw['thumbnail']) > 0:
        if 'url' in raw['thumbnail'][0]:
            obj.visual = raw['thumbnail'][0]['url']
    elif 'enclosure' in raw and len(raw['enclosure']) > 0:
        if 'href' in raw['enclosure'][0]:
            obj.visual = raw['enclosure'][0]['href']
    elif 'visual' in raw and 'url' in raw['visual']:
        obj.visual = raw['visual']['url']
    if obj.visual.lower().strip() == 'none':
        obj.visual = ''

    # Collect text in nested JSON content
    if 'content' in obj.raw:
        obj.content = obj.raw['content']
    else:
        if 'summary' in obj.raw:
            if 'content' in obj.raw['summary']:
                obj.content = obj.raw['summary']['content']
            else:
                obj.content = obj.raw['summary']
        else:
            obj.content = ''

    # Detect language
    obj.lang = guess_language(obj.content) or ''

    # Collect tags
    tags = []
    if 'tags' in obj.raw:
        for tag in obj.raw['tags']:
            if 'label' in tag:
                label = tag['label'].replace(',','-')
                label = label.strip().lower()
                if len(label) > 3 and not label in tags:
                    tags.append(label)
        obj.tags = ','.join(tags)

    return obj
