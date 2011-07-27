###
# Copyright (c) 2011, David Stillman
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

import simplejson
import supybot.utils.web as web
import urllib2
from urllib import urlencode, quote
import httplib
from BeautifulSoup import BeautifulStoneSoup as BSS
from random import randint

SNARFERS = ['bit.ly','goo.gl','is.gd','ow.ly','tinyurl.com','tr.im','youtu.be']

class ShortUrlSnarfer(callbacks.Plugin):

    regexps = ['shortUrlSnarfer']

    def shortUrlSnarfer(self, irc, msg, match):
        r'https?://(binged.it|bit.ly|fb.me|goo.gl|is.gd|ow.ly|su.pr|tinyurl.com|tr.im|youtu.be)(/[^\s,;.]+)'
        domain = match.group(1)
        path = match.group(2)
        conn = httplib.HTTPConnection(domain)
        conn.request("HEAD", path)
        res = conn.getresponse()
        print res.status
        if res.status == 301 or res.status == 302:
            resolved = res.getheader('location')
        irc.reply('expanded: ' + resolved, prefixNick=True)

Class = ShortUrlSnarfer


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
