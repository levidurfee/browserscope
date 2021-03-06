#!/usr/bin/python2.5
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

"""Benchmark Tests Definitions."""

import logging

from categories import test_set_base


_CATEGORY = 'v8'


class V8Test(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc):
    """Initialze a benchmark test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      doc: a description of the test
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        doc=doc,
        min_value=0,
        max_value=60000)


_TESTS = (
  # key, name, doc
  V8Test(
    'Richards', 'Richards', 'OS kernel simulation benchmark, originally written in BCPL by Martin Richards (<i>539 lines</i>).'
  ),
  V8Test(
    'DeltaBlue', 'DeltaBlue', 'One-way constraint solver, originally written in Smalltalk by John Maloney and Mario Wolczko (<i>880 lines</i>).'
  ),
  V8Test(
    'Crypto', 'Crypto', 'Encryption and decryption benchmark based on code by Tom Wu (<i>1698 lines</i>).'
  ),
  V8Test(
    'RayTrace', 'RayTrace', 'Ray tracer benchmark based on code by <a href="http://flog.co.nz/">Adam Burmister</a> (<i>935 lines</i>).'
  ),
  V8Test(
    'EarleyBoyer', 'EarleyBoyer', 'Classic Scheme benchmarks, translated to JavaScript by Florian Loitsch\'s Scheme2Js compiler (<i>4685 lines</i>).'
  ),
  V8Test(
    'RegExp', 'RegExp', 'Regular expression benchmark generated by extracting regular expression operations from 50 of the most popular web pages (<i>1614 lines</i>).'
  ),
  V8Test(
    'Splay', 'Splay', 'Data manipulation benchmark that deals with splay trees and exercises the automatic memory management subsystem (<i>378 lines</i>).'
  ),
  V8Test(
    'Overall', 'Overall Score', 'The overall score for all V8 Benchmark tests'
  ),
)


class V8TestSet(test_set_base.TestSet):

  def GetTestScoreAndDisplayValue(self, test, raw_scores):
    """Get a normalized score (0 to 100) and a value to output to the display.

    Args:
      test_key: a key for a test_set test.
      raw_scores: a dict of raw_scores indexed by test keys.
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.
    """
    raw_score = raw_scores.get(test_key, None)
    if raw_score:
      return raw_score, raw_score
    else:
      return 0, ''


TEST_SET = V8TestSet(
    category=_CATEGORY,
    category_name='V8 Benchmark',
    summary_doc='A collection of pure JavaScript benchmarks that the V8 team has used to tune V8.',
    subnav={
      'Test': '/%s/test' % _CATEGORY,
      'About': '/%s/about' % _CATEGORY,
    },
    home_intro = '''This is the V8 benchmark suite: A collection of pure JavaScript
benchmarks that the V8 team has used to tune V8.
V8 benchmarks reflect pure JavaScript performance while web applications running in a
web browser have tasks other than JavaScript to contend with, such as: waiting for a
network connection, manipulating the Document Object Model and rendering pages.
<a href="/v8/about">Read more about the V8 benchmark suite tests.</a>''',
    tests=_TESTS
)
