#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import opml

if len(sys.argv) < 2:
    print('Usage: import_opml.py <path_to_file>')
    sys.exit(1)

result = []
feeds = opml.parse(sys.argv[1])
for outline in feeds:
    if len(outline) > 0:
        for feed in outline:
            if feed.type == 'rss':
                result.append({'title': feed.text, 'url': feed.xmlUrl})
    else:
        if outline.type == 'rss':
            result.append({'title': outline.text, 'url': outline.xmlUrl})
print(result)
