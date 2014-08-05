#!/sevabot

# -*- coding: utf-8 -*-

"""
Simple <title> grabber
"""

from mechanize import Browser
import urllib2
import web

br = Browser()
urlsh = "http://www.google.com/"
br.open(urlsh)
title = br.title()

def short(text):
    """
    This function creates a bitly url for each url in the provided string.
    The return type is a list.
    """
    ## make sure that it is not already a bitly shortened link
    if '/j.mp' not in text and '/bit.ly' not in text and '/bitly.com' not in text:
        longer = urllib2.quote(text)
        url = 'http://api.j.mp/v3/shorten?login=linkitio'
        url += '&apiKey=R_e6eb9e802a029571a9715963d66f3b84&longUrl='+ longer +'&format=txt'
        shorter = web.get(url)
        shorter.strip()
        return shorter
    else:
        return False


print short(urlsh)

