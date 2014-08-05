#!/sevabot

# -*- coding: utf-8 -*-

"""
Simple help tool
"""
from __future__ import unicode_literals

import os
import Skype4Py
import logging

from collections import OrderedDict
from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id

logger = logging.getLogger("Titles")

# Set to debug only during dev
logger.setLevel(logging.INFO)

logger.debug("Titles module level load import")

HELP_TEXT = """I was made by mikemike, but don't pester him, he's busy."""

class HelpHandler(StatefulSkypeHandler):

    """
    Skype message handler class for the help.
    """

    def __init__(self):
        """
        Use `init` method to initialize a handler.
        """

        logger.debug('Titles handler constructed')

    def init(self, sevabot):
        """
        Set-up our state. This is called every time module is (re)loaded.

        :param skype: Handle to Skype4Py instance
        """

        logger.debug('Help intialized')

        self.sevabot = sevabot
        self.commands = {
            'help': self.help
        }
        
        logger.debug('Help finished initializing')

    def handle_message(self, msg, status):
        """
        Override this method to customize a handler.
        """
        body = ensure_unicode(msg.Body)

        # Parse the chat message to commanding part and arguments
        words = body.split(" ")
        lower = body.lower()

        if len(words) == 0:
            return False

        # Parse argument for two part command names
        if len(words) >= 2:
            desc = " ".join(words[2:])
        else:
            desc = None

        chat_id = get_chat_id(msg.Chat)

        # Check if we match any of our commands
        for name, cmd in self.commands.items():
            if lower.startswith(name):
                cmd(msg, status, desc, chat_id)
                return True

        return False

    def shutdown():
        """
        Called when the module is reloaded.
        """

    def help(self, msg, status, desc, chat_id):
        """
        Show help message to the sender.
        """
        # Make sure we don't trigger ourselves with the help text
        if not desc:
            msg.Chat.SendMessage(HELP_TEXT)

# Export the instance to Sevabot
sevabot_handler = HelpHandler()

__all__ = ['sevabot_handler']
