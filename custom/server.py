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

    if(ip == '188.65.118.238'):
        print(host + ' is on the RNM Test server ('+ ip +')')
    elif(ip == '91.146.111.9' or ip == '91.146.111.186'):
        print(host + ' is on the RNM Test 2 server ('+ ip +')')
    elif(ip == '91.208.99.12'):
        print(host + ' is on the Cloud servers ('+ ip +')')
    elif(ip == '188.65.114.182'):
        print(host + ' is on the Varnish reverse proxy on the Cloud servers ('+ ip +')')
    else:
        print(host + " doesn't appear to be on any of the Reckless servers, but it could be on a weird IP due to SSL. Maybe.")

