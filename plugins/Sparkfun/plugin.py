###
# Copyright (c) 2011, SparkFun
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


import re
import cgi
import time
import socket
import urllib

import supybot
import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

simplejson = None

try:
    simplejson = utils.python.universalImport('json')
except ImportError:
    pass

try:
    if simplejson is None or hasattr(simplejson, 'read'):
        simplejson = utils.python.universalImport('simplejson',
                                                  'local.simplejson')
except ImportError:
    raise callbacks.Error, \
            'You need Python2.6 or the simplejson module installed to use ' \
            'this plugin.  Download the module at ' \
            '<http://undefined.org/python/#simplejson>.'

# Use this for the version of this plugin.  You may wish to put a CVS keyword
# in here if you're keeping the plugin in CVS or some similar system.
__version__ = ""

# XXX Replace this with an appropriate author or supybot.Author instance.
__author__ = supybot.authors.unknown

# This is a dictionary mapping supybot.Author instances to lists of
# contributions.
__contributors__ = {}

# This is a url where the most recent plugin package can be downloaded.
__url__ = '' # 'http://supybot.com/Members/yourname/Sparkfun/download'

import config
import plugin
reload(plugin) # In case we're being reloaded.
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if world.testing:
    import test

class Sparkfun(callbacks.PluginRegexp): 
    regexps = ['sparkfunSnarfer'] 
 
    def sparkfunSnarfer(self, irc, msg, match): 
        r'https?://(www\.)?(sparkfun|sprkfn)\.com(.*)'
        dom = match.group(2)
        url = match.group(3) 
        if 'sprkfn' == dom:
            print 'sprkfn'
        elif 'sparkfun' == dom:
            m = re.match(r"/(\w+)/(\w+)/?", url)
            if not m:
                return
            if 'products' == m.group(1) and m.group(2).isdigit():
                data = self.getproduct(m.group(2), msg.args[0])
                if not data['id'].isdigit():
                    irc.reply('that product does not exist!')
                    return
                irc.reply(data['name'] + ' [ http://sprkfn.com/' + data['id'] + ' ]')
            elif 'news' == m.group(1) and m.group(2).isdigit():
                data = self.getnews(m.group(2), msg.args[0])
                if not data['news_id'].isdigit():
                    irc.reply('that news post does not exist!')
                    return
                irc.reply(data['news_title'] + ' [ http://sprkfn.com/n' + data['news_id'] + ' ]')
    sparkfunSnarfer = urlSnarfer(sparkfunSnarfer) 

    def parseurl(self, url, channel):
        return
 
    def getproduct(self, product, channel): 
        try:
            fd = utils.web.getUrlFd('http://www.sparkfun.com/products/' + product + '.json') 
        except utils.web.Error, e:
            return False
        json = simplejson.load(fd) 
        fd.close() 
        return json
 
    def getnews(self, newsid, channel): 
        fd = utils.web.getUrlFd('http://www.sparkfun.com/news/' + newsid + '.json') 
        json = simplejson.load(fd) 
        fd.close() 
        return json
 
    def searchproduct(self, product, channel): 
        fd = utils.web.getUrlFd('http://www.sparkfun.com/search/results.json?what=products&term=' + urllib.quote(product)) 
        json = simplejson.load(fd) 
        fd.close() 
        return json

    def search(self, irc, msg, args, text):
        channel = msg.args[0]
        data = self.searchproduct(text, ' '.join(msg.args))
        if 'true' == data['success']:
            irc.reply('top result: ' + data['results'][0]['products_name'] + ' [ ' + data['results'][0]['products_link'] + ' ]')
        else:
            irc.reply('nothing found :(')
    search = wrap(search, ['text'])

    def sparkfun(self, irc, msg, args, text):
        if text.isdigit():
            data = self.getproduct(text, msg.args[0])
            if not data:
                irc.error('that product does not exist!')
                return
            if not data['id'].isdigit():
                irc.error('that product does not exist!')
                return
            irc.reply(data['name'] + ' [ http://sprkfn.com/' + data['id'] + ' ]')
    sparkfun = wrap(sparkfun, ['text'])

Class = Sparkfun
configure = config.configure

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

