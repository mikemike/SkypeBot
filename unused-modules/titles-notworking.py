#!/sevabot

# -*- coding: utf-8 -*-

"""
Simple <title> grabber
"""
from __future__ import unicode_literals

import re
import os
import Skype4Py
import logging
import urllib2
import web

from collections import OrderedDict
from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id

IGNORE = list()

logger = logging.getLogger("Titles")

# Set to debug only during dev
logger.setLevel(logging.INFO)

logger.debug("Titles module level load import")

class TitleHandler(StatefulSkypeHandler):

    """
    Skype message handler class for the conference call hosting.
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

        logger.debug('Titles intialized')

        self.sevabot = sevabot
        
        logger.debug('Titles finished initializing')

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
            msg.Chat.SendMessage(title + ' - ' + text)
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
        uri = url
        
        logging.warning('here 1')       
 
        for item in IGNORE:
            if item in uri:
                return False, 'ignored'

        if not re.search('^((https?)|(ftp))://', uri):
            uri = 'http://' + uri

        if 'twitter.com' in uri or 'google.com' in uri:
            uri = uri.replace('#!', '?_escaped_fragment_=')

        if 'i.imgur' in uri:
            a = uri.split('.')
            uri = a[0][:-1] + '.'.join(a[1:-1])

        if 'zerobin.net' in uri:
            return True, 'ZeroBin'

        #uri = uc.decode(uri)
        logging.warning('here 2')
        ## proxy the lookup of the headers through .py
        def remote_call():
            pyurl = u'https://tumbolia.appspot.com/py/'
            code = 'import simplejson;'
            code += "req=urllib2.Request(%s, headers={'Accept':'*/*'});"
            code += "req.add_header('User-Agent', 'Mozilla/5.0');"
            code += "u=urllib2.urlopen(req);"
            code += "rtn=dict();"
            code += "rtn['headers'] = u.headers.dict;"
            code += "contents = u.read();"
            code += "con = str();"
            code += r'''exec "try: con=(contents).decode('utf-8')\n'''
            code += '''except: con=(contents).decode('iso-8859-1')";'''
            code += "rtn['read'] = con;"
            code += "rtn['url'] = u.url;"
            code += "rtn['geturl'] = u.geturl();"
            code += "print simplejson.dumps(rtn)"
            query = code % repr(uri)
            temp = web.quote(query)
            u = web.get(pyurl + temp)

            try:
                useful = json.loads(u)
                return True, useful
            except Exception, e:
                #print "%s -- Failed to parse json from web resource. -- %s" % (time.time(), str(e))
                return False, str(u)

        status = False
        k = 0
        logging.warning('here 3')
        error_num = re.compile('HTTPError: HTTP Error (\S+):')
        error_codes = ['301', '302', '403', '404', '410']
        msg = str()
        while not status:
            status, msg = remote_call()

            if status:
                break

            txt = error_num.findall(msg)
            if txt:
                txt = txt[0]
                try:
                    txt = int(txt)
                except:
                    break
                if 500 <= txt <= 599:
                    break
                if txt in error_codes:
                    break

            k += 1

            if k >= 5:
                break
            time.sleep(0.5)

        if not status:
            return False, msg

        logging.warning('here 4')
        useful = msg

        info = useful['headers']
        page = useful['read']

        try:
            mtype = info['content-type']
        except:
            print 'failed mtype:', str(info)
            return False, 'mtype failed'
        if not (('/html' in mtype) or ('/xhtml' in mtype)):
            return False, str(mtype)

        logging.warning('here 5')
        content = page
        regex = re.compile('<(/?)title( [^>]+)?>', re.IGNORECASE)
        content = regex.sub(r'<\1title>', content)
        regex = re.compile('[\'"]<title>[\'"]', re.IGNORECASE)
        content = regex.sub('', content)
        start = content.find('<title>')
        if start == -1:
            return False, 'NO <title> found'
        end = content.find('</title>', start)
        if end == -1:
            return False, 'NO </title> found'
        content = content[start + 7:end]
        content = content.strip('\n').rstrip().lstrip()
        title = content

        logging.warning('here 6')

        if len(title) > 200:
            title = title[:200] + '[...]'

        title = title.replace('\n', '')
        title = title.replace('\r', '')

        logging.warning('here 7')

        def remove_spaces(x):
            if '  ' in x:
                x = x.replace('  ', ' ')
                return remove_spaces(x)
            else:
                return x

        title = remove_spaces(title)

        new_title = str()
        for char in title:
            unichar = uc.encode(char)
            if len(list(uc.encode(char))) <= 3:
                new_title += uc.encode(char)
        title = new_title

        logging.warning('here 8')

        title = re.sub(r'(?i)dcc\ssend', '', title)

        if title:
            return True, title
        else:
            return False, 'No Title'


# Export the instance to Sevabot
sevabot_handler = TitleHandler()

__all__ = ['sevabot_handler']
