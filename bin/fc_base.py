"""
Load the font correctors

This is a basic font corrector, accumulated from experiences with several
volumes (especially Diplomata and Constitutiones).

Be advised, this font correction is only expected to be of any value
in the context of PDFs from the MGH.

This file contains an abstract base class ``FontCorrector``. The only
FontCorrector that is derived from this class as of now is the
``DiplomataCorrector``. We expect further input which will either
amend (and thus generalize) the ``DiplomataCorrector`` or it will result
in the establishment of another (improved and differenct) Corrector.

Usage:

The ``anapdf`` and ``pdf2tei`` scripts accept an option ``-c, --cor,
--corrector`` which expects the filename of a Python file with the
font corrector loader (path to this file). When ``pdfminer`` has loaded
the fonts from the PDF file, the function ``fc_loader`` will be called.

The ``fc_loader`` is supposed to return a list of ``FontCorrector``
instances. They will be each in turn applied to the fonts loaded from
the PDF file.

A FontCorrector is a class that can be initialized without arguments
and has a method ``correct(font)`` which takes a single instance of
``pdfminer.pdffont.PDFFont`` as input and modifies it in place.

For the time being, the ``FontCorrector`` and the ``FontCorrectorError``
are not included with the code base of PDFMiner but have to be defined
here. This will probably change in the future.
"""

import logging

def fc_loader():
    fc = BaseCorrector()
    return [fc]

class FontCorrectorError(Exception): pass

class FontCorrector(object):

    def correct(self, font):
        raise NotImplementedError

# Swapping tables for BaseCorrector

swaptables = {
    "ATGarSo": {
        u"\u0065": (u"\u0119", 101),
    },
    "ATGarSo-Italic": {
        u"\u0065": (u"\u0119", 101),
    },
    "GriechischItalic": {
        u"\u0049": (u"\u0399", 73),
        u"\u0056": (u"\u03db", 86),
        u"\u0061": (u"\u03b1", 97),
        u"\u006b": (u"\u03ba", 107),
        u"\u006f": (u"\u03bf", 111),
        u"\u0072": (u"\u03c1", 114),
        u"\u0073": (u"\u03c3", 115),
        u"\u00e1": (u"\u03ac", 225),
        u"\u00fa": (u"\u03cd", 250),
        u"\u2019": (u"\u0313", 146),
    },
    "GriechischMedium": {
        u"\u002a": (u"\u1fbf", 42),
        u"\u0041": (u"\u0391", 65),
        u"\u0056": (u"\u03c2", 86),
        u"\u0068": (u"\u03b7", 104),
        u"\u006d": (u"\u03bc", 109),
        u"\u0072": (u"\u03c1", 114),
        u"\u00e2": (u"\u1fb6", 226),
    },
    "PSMT": {
        u"": (u"\u0302", 26),
    },
    "Spezialzeichen": {
        u"\u0032": (u"\u25cb", -1),  # white circle
        u"\u0033": (u"\u25d2", -1),  # circle with lower half black
        u"\u0034": (u"\u25d4", -1),  # circle with upper right quadrant black
                                     # NB: should actually be: circle with
                                     # lower right quadrant black
        u"\u0035": (u"\u25d5",  -1), # circle with all but upper left quadrant
                                     # black
                                     # NB: should actually be: circle with all
                                     # but lower right quadrant black
    },
    "STGSneu-Italic": {
        u"\u004b": (u"\u1e32", 75),
        u"\u0067": (u"\u0121", 103),
        u"\u006b": (u"\u1e33", 107),
        u"\u00d8": (u"\u1e6c", 216),
    },
    "STGSneu-Roman": {
        u"\u0068": (u"h\u032f", 104),
        u"\u00d3": (u"O\u0367", 211),
        u"\u00f2": (u"o\u036e", 242),
    },
    "STGSneu2-Italic": {
        u"\u0061": (u"\u0101", 97),
        u"\u006f": (u"\u014d", 111),
    },
    "STGSneu2-Roman": {
        u"\u0061": (u"\u0101", 97),
        u"\u0069": (u"\u012b", 105),
        u"\u006f": (u"\u014d", 111),
        u"\u0070": (u"p\u0304", 112),
    },
    "StGS4-Roman": {
        u"\u00f2": (u"o\u0367", 242),
    },
    "StGSonderItalic": {
        u"\u0047": (u"\u01e6", 71),
        u"\u0048": (u"\u1e24", 72),
        u"\u0053": (u"\u1e62", 83),
        u"\u0065": (u"\u0119", 101),
        u"\u0068": (u"\u1e25", 104),
        u"\u0074": (u"\u1e6d", 116),
        u"\u00d3": (u"\u01d1", 211),
        u"\u00df": (u"\u0143", 223),
        u"\u00e3": (u"\u0101", 227),
        u"\u00e7": (u"\u010d", 231),
        u"\u00ea": (u"\u011b", 234),
        u"\u00ee": (u"\u012b", 238),
        u"\u00f0": (u"\u0161", 240),
        u"\u00f7": (u"\u0159", 247),
        u"\u00f8": (u"\u1e63", 248),
        u"\u00fc": (u"\u016b", 252),
        u"\u2021": (u"\u0142", 135),
    },
    "StGSonderRoman": {
        u"\u0047": (u"\u01e6", 71),
        u"\u0048": (u"\u1e24", 72),
        u"\u0053": (u"\u1e62", 83),
        u"\u0065": (u"\u0119", 101),
        u"\u0068": (u"\u1e25", 104),
        u"\u0074": (u"\u1e6d", 116),
        u"\u00ae": (u"\u1e6f", 174),
        u"\u00d3": (u"\u01d1", 211),
        u"\u00da": (u"U\u0366", 218),
        u"\u00e3": (u"\u0101", 227),
        u"\u00ee": (u"\u012b", 238),
        u"\u00f2": (u"o\u0364", 242),
        u"\u00f3": (u"\u01d2", 243),
        u"\u00f8": (u"\u1e63", 248),
        u"\u00f9": (u"u\u0364", 249),
        u"\u00fa": (u"u\u0366", 250),
        u"\u00fc": (u"\u016b", 252),
    },
    "StempelGaramondLTPro-Bold": {
        u"\u016f": (u"u\u0366", 31),
    },
    "StempelGaramondLTPro-Italic": {
        u"\u00e1": (u"\u00c1", 127),
    },
    "StempelGaramondLTPro-Roman": {
        u"\u016f": (u"u\u0366", 29),
        u"\u016f": (u"u\u0366", 31),
    },
    "SwisSo-Italic": {
        u"\u0065": (u"\u0119", 101),
    },
    "SwisSo-Roman": {
        u"\u0045": (u"\u0118", 69),
        u"\u0065": (u"\u0119", 101),
    },
    "Symbol": {
        u"": (u"\u2192", 109),  # right arrow
        u"\u0051": (u"\u0398", 52),  # Theta
    },
    "TimesNewRomanPS-ItalicMT": {
        u"\u0131": (u"\u00ed", 213),
        u"\u016f": (u"u\u0366", 292),
        u"\u02db": (u"\u0105", 222),
    },
    "TimesNewRomanPSMT": {
        u"\u00ad": (u"τ\u00ad", 3),
    },
    "TimesSonder-Italic": {
        u"\u0023": (u"\u0158", 35),
        u"\u006c": (u"\u0142", 108),
        u"\u006e": (u"\u0144", 110),
        u"\u0072": (u"\u0159", 114),
        u"\u00a4": (u"\u015b", 130),
        u"\u00e6": (u"\u011b", 230),
        u"\u00f7": (u"\u010c", 247),
        u"\u00fa": (u"u\u0366", 250),
        u"\u0152": (u"u\u0364", 140),
        u"\u0160": (u"\u015a", 138),
        u"\u0161": (u"\u010d", 154),
    },
    "TimesSonder-Roman": {
        u"\u003e": (u"V\u0302", 62),
        u"\u0056": (u"V\u030a", 86),
        u"\u0058": (u"\u25b2", -1),
        u"\u005a": (u"\u017d", 90),
        u"\u0065": (u"\u0119", 101),
        u"\u006c": (u"\u0142", 108),
        u"\u006f": (u"ı\u0366", 111),
        u"\u0072": (u"\u0159", 114),
        u"\u0075": (u"u\u0364", 117),
        u"\u0076": (u"v\u0366", 118),
        u"\u0077": (u"w\u0364", 119),
        u"\u0078": (u"\u25b2", 120),
        u"\u0079": (u"v\u0302", 121),  # older context had: u"\u0079": (u"\u0177", 121),
        u"\u007a": (u"\u017e", 122),
        u"\u007d": (u"v\u0364", 125),
        u"\u00a9": (u"W\u0366", 169),
        u"\u00d2": (u"\u01d1", 210),
        u"\u00d3": (u"O\u0364", 211),
        u"\u00d4": (u"\u01d1", -1),
        u"\u00da": (u"\u016e", -1),
        u"\u00e0": (u"a\u0364", -1),
        u"\u00e2": (u"\u01ce", 226),
        u"\u00e6": (u"\u011b", 230),
        u"\u00ed": (u"i\u0364", -1),
        u"\u00ee": (u"\u01d0", 238),
        u"\u00f0": (u"r\u0364", -1),
        u"\u00f2": (u"o\u036e", 242),
        u"\u00f4": (u"\u01d2", -1),
        u"\u00f6": (u"o\u0364", 246),
        u"\u00f7": (u"\u010c", 247),
        u"\u00fa": (u"u\u0366", 250),
        u"\u0131": (u"i\u0366", 7),
        u"\u0152": (u"u\u0364", 140),
        u"\u0161": (u"\u010d", 157),
        u"\u2122": (u"i\u036e", 146),  # (i with caron (U+01D0)?)
    },
    "TimesSonder2": {
        u"\u0061": (u"\u0363", CID: 97),
        u"\u00b0": (u"\u030a", CID: 176),
    },
    "TimesSonder3": {
        u"\u003e": (u"V\u0302", 62),
        u"\u0066": (u"f\u0364", 102),
        u"\u0067": (u"g\u0364", 103),
        u"\u006d": (u"m\u0364", 109),
        u"\u0072": (u"r\u0366", 114),
        u"\u0073": (u"s\u0364", 115),
        u"\u0074": (u"t\u0364", 116),
        u"\u0075": (u"u\u0364", 117),
        u"\u0077": (u"w\u0367", 119),
        u"\u0079": (u"v\u030a", 121),
        u"\u007a": (u"z\u0364", 122),
        u"\u007d": (u"w\u0366", 125),
        u"\u00a9": (u"W\u0366", 169),
        u"\u00b0": (u"a\u1de0", 176),
        u"\u00b2": (u"v\u0364", 178),
        u"\u00b3": (u"\u1eb9", 179),
        u"\u00bb": (u"w\u036e", 187),
        u"\u00bc": (u"v\u0302", 188),
        u"\u00d2": (u"O\u0367", 210),
        u"\u00d3": (u"O\u0364", 211),
        u"\u00d7": (u"u\u0365", 215),
        u"\u00da": (u"U\u0366", 218),
        u"\u00dc": (u"U\u0364", 220),
        u"\u00e0": (u"a\u0364", 224),
        u"\u00e1": (u"a\u0366", 225),
        u"\u00e2": (u"a\u0367", 226),
        u"\u00e4": (u"a\u036e", 228),
        u"\u00e8": (u"e\u036e", 232),
        u"\u00eb": (u"e\u0364", 235),
        u"\u00ed": (u"i\u0364", 237),
        u"\u00f0": (u"r\u0364", 240),
        u"\u00f1": (u"n\u0364", 241),
        u"\u00f2": (u"o\u0366", 242),
        u"\u00f3": (u"o\u0367", 243),
        u"\u00f6": (u"o\u0364", 246),
        u"\u00fb": (u"\u01d4", 251),
        u"\u00fd": (u"y\u0364", 253),
        u"\u0152": (u"u\u0364", -1),
        u"\u2022": (u"u\u0365", 244),
    },
    "TimesSonder3-Italic": {
        u"\u0052": (u"\u0158", 82),
        u"\u005a": (u"\u017b", 90),
        u"\u00a4": (u"\u0161", 130),
        u"\u00d0": (u"\u017c", 208),
        u"\u00e5": (u"\u0105", 229),
    },
    "TimesSonder4": {
        u"\u00f9": (u"u\u0365", 5),
    },
    "Wingdings2": {
        u"\u00cb": (u"\u2020", 173),
    },
}


class BaseCorrector(FontCorrector):

    def __init__(self):
        self.sonder_roman_swap = { # OK
                u"\u0058": u"\u25b2",  # elongata
                u"\u00e0": u"a\u0364",
                u"\u0075": u"u\u0364",  # CID: 117
                u"\u00a9": u"W\u0366",  # CID: 169
                u"\u00d4": u"\u01d1",
                u"\u00da": u"\u016e",
                u"\u00ed": u"i\u0364",
                u"\u00f0": u"r\u0364",
                u"\u00f4": u"\u01d2",
                u"\u003e": u"V\u0302",  # CID: 62
                u"\u0056": u"V\u030a",  # CID: 86
                u"\u005a": u"\u017d",  # CID: 90
                u"\u0065": u"\u0119",  # CID: 101
                u"\u006c": u"\u0142",  # CID: 108
                u"\u0072": u"\u0159",  # CID: 114
                u"\u0076": u"v\u030a",  # CID: 118
                u"\u0077": u"w\u0364",  # CID: 119
                u"\u0078": u"\u25b2",  # CID: 120 (elongata)
                u"\u0079": u"v\u0302",  # CID: 121
                u"\u007a": u"\u017e",  # CID: 122
                u"\u007d": u"v\u0364",  # CID: 125
                u"\u2122": u"i\u036e",  # CID: 146 (i with caron (U+01D0)?)
                u"\u0152": u"u\u0364",  # CID: 150
                u"\u0161": u"\u010d",  # CID: 157
                u"\u00d2": u"\u01d1",  # CID: 210
                u"\u00e2": u"\u01ce",  # CID: 226
                u"\u00e6": u"\u011b",  # CID: 230
                u"\u00ee": u"\u01d0",  # CID: 238
                u"\u00f2": u"\u01d2",  # CID: 242
                u"\u00f6": u"o\u0364",  # CID: 246
                u"\u00f7": u"\u010c",  # CID: 247
                u"\u00fa": u"\u016f",  # CID: 250
            }
        self.sonder_roman2_swap = { # OK
                u"a": u"\u0363",  # CID: 97
                u"e": u"e",  # CID: 101
                u"y": u"y",  # CID: 121
                u"\u00b0": u"\u030a",  # CID: 176
            }
        self.sonder_roman3_swap = { # OK
                u"\u003e": u"V\u0302",  # CID: 62
                u"\u0075": u"u\u0364",  # CID: 117
                u"\u0079": u"v\u030a",  # CID: 121
                u"\u00a9": u"W\u0366",  # CID: 169
                u"\u00bc": u"v\u0302",  # CID: 188
                u"\u00d3": u"O\u0364",  # CID: 211
                u"\u00da": u"\u016e",  # CID: 218
                u"\u00f6": u"o\u0364",  # CID: 246
            }
        self.griechisch_medium_swap = { # OK
                u"\u002a": u"\u1fbf",  # CID: 42
                u"\u0041": u"\u0391",  # CID: 65
                u"\u0056": u"\u03c2",  # CID: 86
                u"\u0068": u"\u03b7",  # CID: 104
                u"\u006d": u"\u03bc",  # CID: 109
                u"\u0072": u"\u03c1",  # CID: 114
                u"\u00e2": u"\u1fb6",  # CID: 226
            }
        self.tt_swap = {
                u"\u00a6": u"\u00a0",  # CID: 166
            }
        self.spezialzeichen_swap = { # OK
                u"2": u"\u25cb",  # white circle
                u"3": u"\u25d2",  # circle with lower half black
                u"4": u"\u25d4",  # circle with upper right quadrant black
                                  # NB: should actually be: circle with
                                  # lower right quadrant black
                u"5": u"\u25d5",  # circle with all but upper left quadrant
                                  # black
                                  # NB: should actually be: circle with all
                                  # but lower right quadrant black
            }
        self.symbol_swap = { # OK
                u"Q": u"\u0398",  # Theta
            }
        self.symbol_cid_swap = { # OK
                109: u"\u2192",  # CID: 109 (right arrow)
                52: u"\u0398",  # Theta
            }
        # This is strange: if we submit an empty dictionary to
        # update the unicode_map of a PDFCIDFont, the unicode
        # conversion will be fine afterwards.
        self.psmt_cid_swap = { # OK
                # 66: u"B",
                26: u"\u0302",  # comibining circumflex accent
            }

    def correct(self, font):
        if self._is_tt_font(font.fontname):
            font.descriptor[u"FontBBox"] = [-198, -247, 1213, 1013]
            font.bbox = font.descriptor[u"FontBBox"]
            font.descriptor[u"Descent"] = -216
            font.descent = font.descriptor[u"Descent"]
            self.reencode(font, self.tt_swap)
        elif "TimesSonder2" in font.fontname:
            self.reencode(font, self.sonder_roman2_swap)
        elif "TimesSonder3" in font.fontname:
            self.reencode(font, self.sonder_roman3_swap)
        elif "TimesSonder" in font.fontname:
            # print(font.descriptor)
            # print(dir(font))
            # adjust some encodings
            self.reencode(font, self.sonder_roman_swap)
        elif "GriechischMedium" in font.fontname:
            self.reencode(font, self.griechisch_medium_swap)
        elif "Spezialzeichen" in font.fontname:
            self.reencode(font, self.spezialzeichen_swap)
        elif self._is_psmt_font(font.fontname):
            self.cid_reencode(font, self.psmt_cid_swap)
        elif self._is_symbol_font(font.fontname):
            try:
                self.reencode(font, self.symbol_swap)
            except FontCorrectorError:
                logging.warning("Trying CID update.")
                self.cid_reencode(font, self.symbol_cid_swap)
        # @@@TODO:
        # Seems a special case with DD PH.
        # Throw it out?
        # 
        # Font metrics:
        # This seems to be a special case with this volume.
        # The metrics of the Sonder-Font seem to be the same
        # as always, but they do not correspond (in this file
        # at least) to the surrounding Times font. So we have
        # to adjust.
        if "TimesSonder" in font.fontname:
            font.descriptor[u"FontBBox"] = [-599, -338, 2031, 1038]
            font.bbox = font.descriptor[u"FontBBox"]
            font.descriptor[u"Descent"] = -307
            font.descent = font.descriptor[u"Descent"]

    def _is_psmt_font(self, fontname):
        # the special case:
        if fontname == "JNNUBF+TimesNewRomanPS-ItalicMT":
            return True
        if fontname == "JNNUBF+StempelGrmnd-Italic":
            return True
        if fontname == "KGLOYZ+StempelGrmnd-Roman":
            return True
        pos1 = fontname.find("PS")
        pos2 = fontname.find("MT")
        if pos1 == -1 or pos2 == -1:
            return False
        if pos2 < pos1:
            return False
        return True

    def _is_symbol_font(self, fontname):
        pos = fontname.find("+")
        return fontname[pos+1:].lower().startswith("symbol")
        
    def _is_tt_font(self, fontname):
        pos = fontname.find("+")
        if pos != -1:
            fontname = fontname[pos + 1:]
        return fontname.startswith("TT")

    def reencode(self, font, swap):
        try:
            ctu = {}
            for k, v in font.cid2unicode.items():
                ctu[k] = swap.get(v, v)
            font.cid2unicode = ctu
            if font.unicode_map:
                font.unicode_map.cid2unichr.update(ctu)
        except AttributeError:
            msg = "Cannot re-encode font {}".format(font.fontname)
            logging.warning(msg)
            raise FontCorrectorError(msg)

    def cid_reencode(self, font, swap):
        try:
            ctu = {}
            for k, v in font.cid2unicode.items():
                ctu[k] = swap.get(k, v)
            font.cid2unicode = ctu
            if font.unicode_map:
                font.unicode_map.cid2unichr.update(ctu)
        except AttributeError:
            # 'PDFCIDFont' object has no attribute 'cid2unicode'
            # so we just try to update directly the unicode_map.
            if font.unicode_map:
                font.unicode_map.cid2unichr.update(swap)
            else:
                logging.warning("Could not re-encode font {}."\
                        .format(font.fontname))
