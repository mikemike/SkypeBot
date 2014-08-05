#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Selects the best person from the chat... honest
"""
import os
from random import choice

names = ['Mike', 'Bryn', 'Kris', 'Dan', 'Geoff']
name = choice(names)
print "It is definitely "+ name +"'s turn to make the tea."
