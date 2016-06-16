#!/usr/bin/env python3
# import cli.app

import time
import datetime
import re
from sys import argv
from os import sep

strTitle = argv[1]
# strFileName = getFileName(strTitle)
lstTitle = re.split('\W', strTitle.lower())
while lstTitle.count(''):
    lstTitle.remove('')
d = datetime.timedelta(seconds = -time.timezone)
n = datetime.datetime.now(datetime.timezone(d))
strFileName = '{}-{}.markdown'.format(n.strftime('%F'), '-'.join(lstTitle))

f = open('_posts{}{}'.format(sep, strFileName), 'w')
print('---', file = f)
print('layout: post', file = f)
print('title: {}'.format(strTitle), file = f)
print('date: {}'.format(n.strftime('%F %T %z')), file = f)
print('categories: ', file = f)
print('---', file = f)