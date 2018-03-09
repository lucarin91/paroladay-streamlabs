# -*- coding: utf-8 -*-
"""
Retrieve and parse the word of the day from https://unaparolaalgiorno.it.
This version of the script use the regex.
"""

import urllib2
import json
import re
import sys

URL = 'https://unaparolaalgiorno.it'
res = urllib2.urlopen(URL)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

data_raw = res.read()
if not data_raw:
    print 'server error'
    exit()

data_raw = unicode(data_raw, "utf-8")

'''
<h2 class="parola">
    <a href="/significato/P/perissologia" rel="bookmark" title="Perissologia">Perissologia</a>
    <span id="word_day">è la parola del giorno</span>
</h2>
'''
reg = '<a href="(/significato/P/([A-z]*))"'
f = re.findall(reg, data_raw)[0]
href = URL + f[0]
parola = f[1][0].upper() + f[1][1:]
# print parola, href

'''
<p class="significato">
    <span class="sign">Sign</span>Enunciazione superflua di cose già espresse
</p>
'''
reg = 'Sign</span>(.*)</p>'
f = re.findall(reg, data_raw)
sign = cleanhtml(f[0])
# print cleanhtml(sign)

'''
<p class="etimo">
    dal greco <i>perissologhìa</i> ‘abbondanza di parole superflue’, derivato da 
    <i>perissològos</i> ‘ciarliero’, composto a sua volta da <i>perissòs</i> 
    ‘che va oltre la norma’ e <i>-loghìa</i>, derivato di <i>lògos</i> ‘parola’.
</p>
'''
reg = '<p class="etimo">(.*)</p>'
f = re.findall(reg, data_raw)
#etim = cleanhtml(f[0]).encode(sys.stdout.encoding, errors='replace')
etim = cleanhtml(f[0])
# print etim

res = u'La parola del giorno è {}. SIGN: {}. ETIM: {} Leggi di più a {}.'.format(
        parola.upper(), sign, etim, href)
print res.encode(sys.stdout.encoding, errors='ignore')

