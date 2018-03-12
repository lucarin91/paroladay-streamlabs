# -*- coding: utf-8 -*-
#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import io
import json
import re
from os.path import isfile
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "ParolaDay"
Website = "https://github.com/lucarin91/parola_streamlabs"
Description = "Return the world of the day."
Creator = "lucarin91"
Version = "1.0.1"

#---------------------------------------
# Set Variables
#---------------------------------------
_command_permission = "everyone"
_command_info = ""
_command = "!parola"
_cooldown = 10

# Internal variables
_re_parola = None
_re_sign = None
_re_etim = None
_re_cleanr =  None

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    global _re_parola, _re_sign, _re_etim, _re_cleanr
    # build regex
    _re_parola = re.compile(r'<a href="(/significato/[A-Z]/([A-z]*))"')
    _re_sign = re.compile(r'Sign</span>(.*)</p>')
    _re_etim = re.compile(r'<p class="etimo">(.*)</p>')
    _re_cleanr = re.compile(r'<.*?>')

    settings = 'Services/Scripts/{}/settings.json'.format(ScriptName)
    if isfile(settings):
        with io.open(settings, mode='r', encoding='utf-8-sig') as f:
            string = f.read()
            Parent.Log(ScriptName, 'Load json: {}'.format(string))
            conf = json.loads(string)
            parse_conf(conf)

    
    
#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    if data.IsChatMessage():
        if data.GetParam(0).lower() == _command\
           and not Parent.IsOnCooldown(ScriptName, _command)\
           and Parent.HasPermission(data.User, _command_permission, _command_info):
            responce = get_parola()
            Parent.SendTwitchMessage(responce)

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
    pass

def Unload():
    pass
    
def ReloadSettings(jsonData):
    parse_conf(json.loads(jsonData))

#---------------------------------------
# My functions
#---------------------------------------
def get_parola():
    """Return the parola of the day."""
    url = 'http://unaparolaalgiorno.it'
    res_raw = Parent.GetRequest(url, {})
    res = json.loads(res_raw)
    status, data = res['status'], res['response']
    if status != 200:
        Parent.Log(ScriptName, 'Request status {}'.format(status))
        return
    
    f = _re_parola.findall(data)[0]
    href = url + f[0]
    parola = f[1][0].upper() + f[1][1:]

    f = _re_sign.findall(data)
    sign = cleanhtml(f[0])

    f = _re_etim.findall(data)
    etim = cleanhtml(f[0])

    res = u'La parola del giorno è {}. SIGN: {}. ETIM: {} Leggi di più a {}'.format(
            parola.upper(), sign, etim, href)
    return res

def parse_conf(conf):
    """Set the configuration variable."""
    global _command, _cooldown
    _command = conf['command']
    _cooldown = conf['cooldown']
    Parent.Log(ScriptName, 'Load conf: {}'.format((_command, _cooldown)))

def cleanhtml(raw_html):
    """Remove HTML tags on a text"""
    cleantext = _re_cleanr.sub('', raw_html)
    return cleantext

def ShowParola():
    """Send the parola of the day to the chat."""
    Parent.Log(ScriptName, 'Send rank to chat!')
    responce = get_parola()
    Parent.SendTwitchMessage(responce)
