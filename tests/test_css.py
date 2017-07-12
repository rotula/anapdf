#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Test CSS parser
"""

import unittest

from anapdf.css import SimpleCSSParser
from anapdf.css import (CSSError,
                        CSSMissingColonError,
                        CSSMissingSemicolonError,
                        CSSIllegalCharacterError,
                        CSSUnexpectedEOFError)

class TestBasic(unittest.TestCase):

    def test_suite(self):
        css = "font-variant: small-caps;\nfont-weight: bold"
        p = SimpleCSSParser(css)
        p.parse()
        d = p.declarations[1]
        self.assertEqual(len(d), 2)

    def test_property(self):
        css = "font-variant: small-caps"
        p = SimpleCSSParser(css)
        p.parse()
        d = p.declarations[0]
        self.assertEqual(d[0], "font-variant")

    def test_expr(self):
        css = "font-variant: small-caps"
        p = SimpleCSSParser(css)
        p.parse()
        d = p.declarations[0]
        self.assertEqual(d[1], "small-caps")

    def test_whites1(self):
        css = "    font-variant     :small-caps   "
        p = SimpleCSSParser(css)
        p.parse()
        d = p.declarations[0]
        self.assertEqual(d[1], "small-caps")

    def test_semicolon(self):
        css = "font-variant: small-caps;"
        p = SimpleCSSParser(css)
        p.parse()
        d = p.declarations[0]
        self.assertEqual(d[1], "small-caps")

    def test_string1(self):
        css = "font-family: 'Garamond'"
        p = SimpleCSSParser(css)
        p.parse()
        d = p.declarations[0]
        self.assertEqual(d[1], "Garamond")

    def test_string2(self):
        css = "font-family: \"Garamond\""
        p = SimpleCSSParser(css)
        p.parse()
        d = p.declarations[0]
        self.assertEqual(d[1], "Garamond")

    def test_missing_colon(self):
        css = "font-style italic"
        p = SimpleCSSParser(css)
        self.assertRaises(CSSMissingColonError, p.parse)

    def test_missing_semicolon(self):
        css = "font-style: italic font-variant: small-caps"
        p = SimpleCSSParser(css)
        self.assertRaises(CSSMissingSemicolonError, p.parse)

    def test_illegal_character(self):
        css = u"fonä-variant: small-caps"
        p = SimpleCSSParser(css)
        self.assertRaises(CSSIllegalCharacterError, p.parse)

    def test_eof1(self):
        css = "font-variant: "
        p = SimpleCSSParser(css)
        self.assertRaises(CSSUnexpectedEOFError, p.parse)

    def test_eof2(self):
        css = "font-variant"
        p = SimpleCSSParser(css)
        self.assertRaises(CSSUnexpectedEOFError, p.parse)

    def test_eof3(self):
        css = "font-family: 'xxx"
        p = SimpleCSSParser(css)
        self.assertRaises(CSSUnexpectedEOFError, p.parse)

