#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Handlers for Network Tests.

Example beacon request:
  http://localhost:8080/beacon?category=network&results=latency=123,hostconn=6,
     maxconn=29,parscript=0,parsheet=1,parcssjs=0,cacheexp=1,cacheredir=0,
     cacheresredir=0,prefetch=1,gzip=1,du=1
"""

__author__ = 'steve@souders.com (Steve Souders)'

#CVSNO - How much of this stuff do I really need?

import time
import datetime
import logging

# Shared stuff
from shared import decorators
from shared import util

from django import http

CATEGORY = 'network'
CATEGORY_NAME = 'Network'

HOME_INTRO = ('A significant performance bottleneck for web pages is network '
  'performance. It\'s true that network performance depends in part on the '
  'user\'s connection speed and geographic location. '
  'But the browser also plays a significant role. '
  'By supporting features such as <code>data:</code> URLs, prefetch links, '
  'and parallel script downloading, browsers can make all web pages load '
  'faster.')

class NetworkTest(object):
  TESTS_URL_PATH = '/%s/tests' % CATEGORY

  def __init__(self, key, label, url, score_type, doc):
    self.key = key
    self.label = label
    self.url = '%s/%s' % (self.TESTS_URL_PATH, url)
    self.score_type = score_type
    self.doc = doc


TESTS = (
  # key, label, url, score_type, doc
  NetworkTest(
    'latency', 'Check Latency', 'latency', 'custom',
    '''add doc'''),
  NetworkTest(
    'hostconn', 'Connections per Hostname', 'connections-per-hostname',
    'custom',
    '''add doc'''),
  NetworkTest(
    'maxconn', 'Max Connections', 'max-connections', 'custom',
    '''add doc'''),
  NetworkTest(
    'parscript', 'Parallel Scripts', 'scripts-block', 'boolean',
    '''add doc'''),
  NetworkTest(
    'parsheet', 'Parallel Stylesheets', 'stylesheets-block', 'boolean',
    '''add doc'''),
  NetworkTest(
    'parcssjs', 'Parallel Stylesheet and Inline Script',
    'inline-script-after-stylesheet', 'boolean',
    '''add doc'''),
  NetworkTest(
    'cacheexp', 'Cache Expires', 'cache-expires', 'boolean',
    '''add doc'''),
  NetworkTest(
    'cacheredir', 'Cache Redirects', 'cache-redirects', 'boolean',
    '''add doc'''),
  NetworkTest(
    'cacheresredir', 'Cache Resource Redirects', 'cache-resource-redirects',
    'boolean' ,
    '''add doc'''),
  NetworkTest(
    'prefetch', 'Link Prefetch', 'link-prefetch', 'boolean',
    '''add doc'''),
  NetworkTest(
    'gzip', 'Compression Supported', 'gzip', 'boolean' ,
    '''add doc'''),
  NetworkTest(
    'du', 'data: URLs', 'data-urls', 'boolean' ,
    '''add doc'''),
)


def CustomTestsFunction(testFieldName, median):
  """Returns a tuple with display text for the cell as well as a 1-100 value.
  i.e. ('1X', 95)
  """
  #logging.info('CustomTestsFunction w/ %s, %s' % (test, median))
  score = 0
  if 'hostconn' == testFieldName:
    if median <= 2:
      score = 60
    elif median <= 4:
      score = 85
    else:
      score = 95
  return str(median), score
  # if test is 'testDisplay':
  #   return median > 100
  # elif test is 'testVisibility':
  #   return median > 200
  # return result


def Render(request, template_file, params):
  """Render network test pages."""

  params['epoch'] = int(time.time())
  return util.Render(request, template_file, params, CATEGORY)


def Home(request):
  """Original index page"""

  params = {
    'page_title': 'Home',
    'stats_table': util.GetStats(request, CATEGORY),
  }
  return Render(request, 'network/home.html', params)


def About(request):
  """About page."""
  params = {
    'page_title': 'Network Tests - About',
    'tests': TESTS,
  }
  return Render(request, 'network/about.html', params)


def Test(request):
  """Network Performance Tests"""

  autorun = request.GET.get('autorun')
  if autorun:
    return http.HttpResponseRedirect('/network/harness')

  params = {
    'page_title': 'Network Performance Tests',
  }
  return Render(request, 'network/test.html', params)


def Harness(request):
  """Network Performance Test Harness"""

  params = {
    'page_title': 'Performance Test Harness',
    'continue': request.GET.get('continue'),
  }
  return Render(request, 'network/harness.html', params)


@decorators.provide_csrf
def TestDriver(request):
  """Network Performance Test Driver"""

  params = {
    'page_title': 'Performance Test Driver',
    'csrf_token': request.session.get('csrf_token'),
    'tests': TESTS,
  }
  return Render(request, 'network/testdriver.html', params)


def Results(request):
  """Network Performance Tests Completed"""

  params = {
    'page_title': 'Performance Tests Completed',
  }
  return Render(request, 'network/results.html', params)


def StatsTable(request):
  params = {
    'stats_table': util.GetStats(request, CATEGORY)
  }
  return Render(request, 'network/stats_table.html', params)


def Faq(request):
  """Network Performance FAQ"""

  params = {
    'page_title': 'Performance FAQ',
  }
  return Render(request, 'network/faq.html', params)


def ParseFix(request):
  """Network Performance Parse Fix XHR"""

  params = {
    'page_title': 'Performance Parse Fix XHR',
  }
  return Render(request, 'network/parse-fix.html', params)


def ParseService(request):
  """Network Performance Parse Web Service"""

  params = {
    'page_title': 'Performance Parse Web Service',
  }
  return Render(request, 'network/parse-service.html', params)


def Parse(request):
  """Network Performance Parse User-Agent"""

  params = {
    'page_title': 'Performance Parse User-Agent',
  }
  return Render(request, 'network/parse.html', params)


def CacheExpires(request):
  """Network Performance Cache Expires Test"""

  params = {
    'page_title': 'Performance Cache Expires Test',
  }
  return Render(request, 'network/tests/cache-expires.html', params)


def CacheExpires2(request):
  """Network Performance Cache Expires Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Cache Expires Test',
    'prevt': prevt,
  }
  return Render(request, 'network/tests/cache-expires2.html', params)


def CacheRedirects(request):
  """Network Performance Cache Redirects Test"""

  params = {
    'page_title': 'Performance Cache Redirects Test',
  }
  return Render(request, 'network/tests/cache-redirects.html', params)


def CacheRedirects2(request):
  """Network Performance Cache Redirects Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Cache Redirects Test',
    'prevt': prevt,
  }
  return Render(request, 'network/tests/cache-redirects2.html', params)


def CacheResourceRedirects(request):
  """Network Performance Cache Resource Redirects Test"""

  params = {
    'page_title': 'Performance Cache Resource Redirects Test',
  }
  return Render(request, 'network/tests/cache-resource-redirects.html', params)


def CacheResourceRedirects2(request):
  """Network Performance Cache Resource Redirects Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Cache Resource Redirects Test',
    'prevt': prevt,
  }
  return Render(request, 'network/tests/cache-resource-redirects2.html', params)


def ConnectionsPerHostname(request):
  """Network Performance Connections per Hostname Test"""

  latency = request.COOKIES.get('latency', 6)
  sleep = min(9, int(2 * round((int(latency) + 500.0) / 1000.0)))

  params = {
    'page_title': 'Performance Connections per Hostname Test',
    'sleep': sleep,
    'latency': latency,
  }
  return Render(request, 'network/tests/connections-per-hostname.html', params)


def DataUrls(request):
  """Network Performance Data URLs Test"""

  params = {
    'page_title': 'Performance Data URLs Test',
  }
  return Render(request, 'network/tests/data-urls.html', params)


def Gzip(request):
  """Network Performance, CATEGORY Gzip Test"""

  # HTTP_ACCEPT_ENCODING is filtered out by App Engine because it
  # handles compression for applications.

  params = {
    'page_title': 'Performance Gzip Test',
  }
  return Render(request, 'network/tests/gzip.html', params)


def InlineScriptAfterStylesheet(request):
  """Network Performance Inline Script After Stylesheet Test"""

  params = {
    'page_title': 'Performance Inline Script After Stylesheet Test',
  }
  return Render(request, 'network/tests/inline-script-after-stylesheet.html', params)


def Latency(request):
  """Network Performance Latency Measurement"""

  params = {
    'page_title': 'Performance Latency Measurement',
  }
  return Render(request, 'network/tests/latency.html', params)


def LinkPrefetch(request):
  """Network Performance Link Prefetch Test"""

  params = {
    'page_title': 'Performance Link Prefetch Test',
  }
  return Render(request, 'network/tests/link-prefetch.html', params)


def LinkPrefetch2(request):
  """Network Performance Link Prefetch Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Link Prefetch Test',
    'prevt': prevt,
  }
  return Render(request, 'network/tests/link-prefetch2.html', params)


def MaxConnections(request):
  """Network Performance Max Connections Test"""

  latency = request.COOKIES.get('latency', 9)
  sleep = max(6, min(9, int(4 * round((int(latency) + 500.0) / 1000.0))))

  params = {
    'page_title': 'Performance Max Connections Test',
    'sleep': sleep
  }
  return Render(request, 'network/tests/max-connections.html', params)


def ScriptsBlock(request):
  """Network Performance Scripts Block Test"""

  params = {
    'page_title': 'Performance Scripts Block Test',
  }
  return Render(request, 'network/tests/scripts-block.html', params)


def StylesheetsBlock(request):
  """Network Performance Stylesheets Block Test"""

  params = {
    'page_title': 'Performance Stylesheets Block Test',
  }
  return Render(request, 'network/tests/stylesheets-block.html', params)


def Admin(request):
  """Network Performance Admin Tools"""

  params = {
    'page_title': 'Performance Admin Tools',
  }
  return Render(request, 'network/admin/admin.html', params)


def ConfirmUa(request):
  """Network Performance Confirm User-Agents"""

  params = {
    'page_title': 'Performance Confirm User-Agents',
  }
  return Render(request, 'network/admin/confirm-ua.html')


def Stats(request):
  """Network Performance Stats"""

  params = {
    'page_title': 'Performance Stats',
    'epoch': epochTime(),
  }
  return util.Render(request, 'network/admin/stats.html', params, CATEGORY)
