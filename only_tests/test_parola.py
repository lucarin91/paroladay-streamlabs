# -*- coding: utf-8 -*-
"""
Retrieve and parse the word of the day from https://unaparolaalgiorno.it.
This version of the script use xPath.
"""

import urllib2
import json
from lxml import html

URL = 'https://unaparolaalgiorno.it'
res = urllib2.urlopen(URL)

data_raw = res.read()
if not data_raw:
    print 'server error'
    exit()

tree = html.fromstring(data_raw)

xpath = '//h2[contains(@class, "parola")]/a'
a = tree.xpath(xpath)
parola = a[0].text
href = URL + a[0].attrib['href']

xpath = '//p[contains(@class, "significato")]'
p = tree.xpath(xpath)
sign = list(p[0].itertext())[1]

xpath = '//p[contains(@class, "etimo")]'
p = tree.xpath(xpath)
etim = ''.join(p[0].itertext())

res = u'La parola del giorno è {}. SIGN: {}. ETIM: {} Leggi di più a {}.'.format(
        parola.upper(), sign, etim, href)
print res

