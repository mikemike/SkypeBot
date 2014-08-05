#!/sevabot

# -*- coding: utf-8 -*-

"""
Simple <title> grabber
"""
from __future__ import unicode_literals

import re
import os
import Skype4Py
import urllib2
import web
import requests

from mechanize import Browser
from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id

class TitleHandler(StatefulSkypeHandler):

    """
    Skype message handler class for the conference call hosting.
    """

    def __init__(self):
        """
        Use `init` method to initialize a handler.
        """

    def init(self, sevabot):
        """
        Set-up our state. This is called every time module is (re)loaded.

        :param skype: Handle to Skype4Py instance
        """
        self.sevabot = sevabot

    def handle_message(self, msg, status):
        """
        Override this method to customize a handler.
        """
        # If you are talking to yourself when testing
        # Ignore non-sent messages (you get both SENDING and SENT events)
        if status == "SENDING" or status == "SENT":
            return

        if status != "RECEIVED":
            return False

        body = ensure_unicode(msg.Body)

        if len(body) == 0:
            return False

        # Check if we match any of our commands
        a = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
        for text in a:
            title = self.find_title(text)
            shortened = self.short(text)
            self.linkitio(text, msg.Sender.FullName)
            if 'youtube.com' in text or 'bbc.co.uk' in text or 'imdb.com' in text:
                if(title):
                    if(shortened):
                        msg.Chat.SendMessage(title + ' - ' + shortened)
                    else:
                        msg.Chat.SendMessage(title + ' - ' + text)
                    return True
                else:
                    return False

        return False

    def shutdown():
        """
        Called when the module is reloaded.
        """

    def find_title(self, url):
        """
        This finds the title when provided with a string of a URL.
        """
        br = Browser()
        br.open(url)
        title = br.title()
        if(title):            
            return title
        else:        
            return False

    def short(self, text):
        """
        This function creates a bitly url for each url in the provided string.
        The return type is a list.
        """
        ## make sure that it is not already a bitly shortened link
        if '/j.mp' not in text and '/bit.ly' not in text and '/bitly.com' not in text:
            longer = urllib2.quote(text)
            url = 'http://api.j.mp/v3/shorten?login=linkitio'
            url += '&apiKey=***&longUrl='+ longer +'&format=txt'
            shorter = web.get(url)
            shorter.strip()
            return shorter
        else:
            return False

    def linkitio(self, url, name):
        """All links are available here: http://skype.linkit.io/"""
        linkiturl = "http://linkit.io/api/post_skype"
        data = {'url':url,'name':name,'pass':'***'}
        r = requests.post(linkiturl, data=data)


# Export the instance to Sevabot
sevabot_handler = TitleHandler()

__all__ = ['sevabot_handler']
