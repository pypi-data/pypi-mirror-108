#!/usr/bin/env python

"""Tests for `parser201` package using individual tests"""

from parser201.parser201 import LogParser

# --------------------------------------------------------------
# Tests
# --------------------------------------------------------------
   
# Verify initilizer behavior with an invalid input type. If any data type other
# than str is passed to the initializer, it should return an object with all
# fields set to None.

def test_badInput():

   L  = {} # Non-str test for initializer
   lp = LogParser(L)

   assert lp.ipaddress   == None
   assert lp.userid      == None
   assert lp.username    == None
   assert lp.timestamp   == None
   assert lp.requestline == None
   assert lp.statuscode  == None
   assert lp.datasize    == None
   assert lp.referrer    == None
   assert lp.useragent   == None

# For complete code coverage, exercise property methods.

def test_setters():
   # This should result in an object with all the fields set to None.
   lp = LogParser('test')

   lp.ipaddress = '192.168.1.1'
   assert lp.ipaddress == '192.168.1.1'

   lp.userid = 'mr-test'
   assert lp.userid == 'mr-test'

   lp.username = 'geozeke'
   assert lp.username == 'geozeke'

   lp.timestamp = '24/Mar/2009:18:07:16 +0100'
   assert lp.timestamp == '24/Mar/2009:18:07:16 +0100'

   lp.requestline = 'GET /images/puce.gif HTTP/1.1'
   assert lp.requestline == 'GET /images/puce.gif HTTP/1.1'

   lp.statuscode = 404
   assert lp.statuscode == 404

   lp.datasize = 20000
   assert lp.datasize == 20000

   lp.referrer = 'Test referrer'
   assert lp.referrer == 'Test referrer'

   lp.useragent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; .NET CLR 1.1.4322)'
   assert lp.useragent == 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; .NET CLR 1.1.4322)'

# --------------------------------------------------------------
