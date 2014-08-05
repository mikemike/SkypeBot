#!/sevabot

# -*- coding: utf-8 -*-

"""
Shows what server a site is on
"""
from __future__ import unicode_literals

import re
import os
import Skype4Py
import urllib2
import socket

from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id

class ServerHandler(StatefulSkypeHandler):

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
            ip = socket.gethostbyname(a)
            msg.Chat.SendMessage('IP is: ' + ip)
            return True
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

# Export the instance to Sevabot
sevabot_handler = TitleHandler()

__all__ = ['sevabot_handler']
