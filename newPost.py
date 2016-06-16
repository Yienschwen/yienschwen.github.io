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
f.write('---\n')
f.write('layout: post\n')
f.write('title: {}\n'.format(strTitle))
f.write('date: {}\n'.format(n.strftime('%F %T %z')))
f.write('categories: \n')
f.write('---\n')
f.close()