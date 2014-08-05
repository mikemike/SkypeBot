#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resolve a host to an IP
"""
from __future__ import absolute_import, division, print_function

import sys
import urllib
import socket
from datetime import datetime, timedelta

def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        return ''

if len(sys.argv) < 2:
    sys.exit("Enter a hostname, like 'rnmtest.co.uk' or 'bbc.co.uk'")

host = sys.argv[1]
ip = resolve_host(host)

if(ip == ''):
    sys.exit("No dice on " + host + " I'm afraid. Make sure you just enter the hostname and don't include http://")
else:
    print("IP of " + host + " is: " + ip)
