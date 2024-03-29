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

from pdfminer.cmapdb import FileUnicodeMap

def fc_loader():
    fc = BaseCorrector()
    return [fc]

class FontCorrectorError(Exception): pass

class FontCorrector(object):

    def correct(self, font):
        raise NotImplementedError

# Swapping tables for BaseCorrector

swaptables = {
    "ATGaramond": {
        u"\u00b0": (u"\u00ba", 176),
        u"\u00c5": (u"A\u0366", 197), 
        u"\u00e5": (u"a\u0366", 229), 
    },
    "ATGaramond-Antiqua": {
        u"\u00b0":  (u"\u00ba", 176),# Ordnungszeichen m�nnlich 
    },
    "ATGaramond-Bold": {
        u"\u00e5": (u"a\u0366", 229),
    },
    "ATGaramond-Italic": {
        # u"\u00b0": (u"\u00ba", 176), nur antizipiert
        # u"\u00c5": (u"A\u0366", 197), nur antizipiert
        u"\u00b0": (u"\u00ba", 176), 
        u"\u00e5": (u"a\u0366", 229),  
    },
    "ATGarSo": {
        u"\u0045": (u"\u0118", 69),
        u"\u0056": (u"V\u0364", 86),
        u"\u0065": (u"\u0119", 101),
        u"\u006a": (u"j\u0364", 106),
        u"\u0076": (u"v\u0364", 118),
        u"\u0079": (u"y\u0364", 121),
        u"\u00c4": (u"A\u0364", 196),   
        u"\u00cb": (u"E\u0364", 203),
        u"\u00d6": (u"O\u0364", 214), 
        u"\u00e4": (u"a\u0364", 228),
        u"\u00e5": (u"a\u0366", 229),
        u"\u00e8": (u"e\u0365", 232),   
        u"\u00e9": (u"e\u0363", 233), 
        u"\u00eb": (u"e\u0364", 235),
        u"\u00ed": (u"i\u0366", 237), 
        u"\u00ef": (u"i\u0364", 239),
        u"\u00f1": (u"n\u0364", 241), 
        u"\u00f3": (u"o\u0363", 243),
        u"\u00f4": (u"o\u036e", 244),                 
        u"\u00f6": (u"o\u0364", 246),
        u"\u00f9": (u"u\u0366", 249),
        u"\u00fb": (u"u\u036e", 251), 
        u"\u00fc": (u"u\u0364", 252),
        u"\u00ff": (u"y\u0366", 255), 
    },
    "ATGarSo-Bold": { 
        u"\u0056": (u"V\u0364", 86), 
        u"\u0076": (u"v\u0364", 118),
        u"\u0079": (u"y\u0364", 121), 
        u"\u00cb": (u"E\u0364", 203),
        u"\u00d6": (u"O\u0364", 214), 
        u"\u00e4": (u"a\u0364", 228),
        u"\u00e8": (u"e\u0365", 232),   
        u"\u00e9": (u"e\u0363", 233), 
        u"\u00eb": (u"e\u0364", 235),
        u"\u00ed": (u"i\u0366", 237), 
        u"\u00ef": (u"i\u0364", 239),
        u"\u00f3": (u"o\u0363", 243),
        u"\u00f4": (u"o\u036e", 244),   
        u"\u00f6": (u"o\u0364", 246),
        u"\u00f9": (u"u\u0366", 249), 
        # u"\u00fb": (u"u\u036e", 251), Nur antizipiert
        u"\u00fc": (u"u\u0364", 252),
    },
    "ATGarSo-BoldItalic": {
        u"\u006c": (u"\u0142", 108),
    },    
    "ATGarSo-Italic": {
        u"\u0056": (u"V\u0364", 86), 
        u"\u0065": (u"\u0119", 101),
        u"\u006c": (u"\u0142", 108),  
        u"\u0076": (u"v\u0364", 118),
        u"\u0079": (u"y\u0364", 121), 
        u"\u00cb": (u"E\u0364", 203),
        u"\u00d6": (u"O\u0364", 214), 
        u"\u00e4": (u"a\u0364", 228),
        u"\u00e5": (u"a\u0366", 229), 
        u"\u00e8": (u"e\u0365", 232),  
        u"\u00e9": (u"e\u0363", 233), 
        u"\u00eb": (u"e\u0364", 235),
        u"\u00ef": (u"i\u0364", 239),
        u"\u00f3": (u"o\u0363", 243),               
        u"\u00f6": (u"o\u0364", 246),
        u"\u00f9": (u"u\u0366", 249), 
        # u"\u00fb": (u"u\u036e", 251), Nur antizipiert
        u"\u00fc": (u"u\u0364", 252), 
    },
    "ATGarSoSC700":   {
        u"\u0045": (u"\u0118", 69),  
    },
    "BLG-GaramondA":  {
        u"\u0061": (u"\u0105", 97),    
    },
    "BLG-GaramondE":  {
        u"\u0043": (u"\u0259", 67),   
    },
    "BLG-GaramondU":  {
        u"\u0039": (u"u\u032f", 57),    
    },
    "Greek":   {
        u"\u005e": (u"\u0311", 94),
        u"\u0063": (u"\u03c7", 99),
        u"\u0065": (u"\u03b5", 101),
        u"\u0069": (u"\u03b9", 105),
        u"\u006e": (u"\u03bd", 110),
        u"\u006f": (u"\u03bf", 111),
        u"\u0070": (u"\u03c0", 112),
        u"\u0072": (u"\u03c1", 114), 
        u"\u0074": (u"\u03c4", 116),
        u"\u0077": (u"\u03c9", 119),
    },
    "GriechischBoldItalic": {
        u"\u0061": (u"\u03b1", 97),
        u"\u0062": (u"\u03b2", 98),
    },
    "GriechischItalic": {  
        u"\u0023": (u"\u1fce", 35), 
        u"\u002b": (u"\u1ffe", 43),
        u"\u0041": (u"\u0391", 65),
        u"\u0042": (u"\u0392", 66),
        u"\u0045": (u"\u0395", 69),
        u"\u0047": (u"\u0393", 71),
        u"\u0048": (u"\u0397", 72), 
        u"\u0049": (u"\u0399", 73),
        u"\u004b": (u"\u039a", 75), 
        u"\u004c": (u"\u039b", 76),
        u"\u004d": (u"\u039c", 77), 
        u"\u004d": (u"\u1ff6", 212),  # Aus BSB 2247
        u"\u004e": (u"\u039d", 78),
        u"\u004f": (u"\u039f", 79),
        u"\u0050": (u"\u03a0", 80), 
        u"\u0053": (u"\u03a3", 83),
        u"\u0056": (u"\u03db", 86),
        u"\u0057": (u"\u03a9", 87),
        u"\u0061": (u"\u03b1", 97),
        u"\u0062": (u"\u03b2", 98),
        u"\u0063": (u"\u03c7", 98),
        u"\u0064": (u"\u03b4", 100),
        u"\u0065": (u"\u03b5", 101),
        u"\u0067": (u"\u03b3", 103),
        u"\u0068": (u"\u03b7", 104),
        u"\u0069": (u"\u03b9", 105),
        u"\u006a": (u"\u03c6", 106),
        u"\u006b": (u"\u03ba", 107),
        u"\u006c": (u"\u03bb", 108),
        u"\u006d": (u"\u03bc", 109),  
        u"\u006e": (u"\u03bd", 110),
        u"\u006f": (u"\u03bf", 111),
        u"\u0070": (u"\u03c0", 112),
        u"\u0072": (u"\u03c1", 114),
        u"\u0073": (u"\u03c3", 115),
        u"\u0074": (u"\u03c4", 116),
        u"\u0075": (u"\u03c5", 117),
        u"\u0076": (u"\u1f14", 118), 
        u"\u0077": (u"\u03c9", 119),
        u"\u0078": (u"\u03be", 120),
        u"\u007a": (u"\u03b6", 122),
        u"\u00a3": (u"\u1f10", 163),
        u"\u00b4": (u"\u0384", 180),
        u"\u00c9": (u"\u03ae", 201),
        u"\u00e1": (u"\u03ac", 225),
        u"\u00e4": (u"\u1f00", 228),  
        u"\u00ea": (u"\u1fc6", 234),
        u"\u00ed": (u"\u03af", 237),
        u"\u00f6": (u"\u1f40", 246), 
        u"\u00fa": (u"\u03cd", 250),
        u"\u00fb": (u"\u1fe6", 251),
        u"\u00fc": (u"\u1f50", 252), 
        u"\u1ff6": (u"\u039c", 77),   
        u"\u2019": (u"\u0313", 146), 
    },
    "GriechischMedium": {
        u"\u0023": (u"\u1fce", 35),
        u"\u002a": (u"\u1fbf", 42),
        u"\u002b": (u"\u1ffe", 43), 
        u"\u0041": (u"\u0391", 65),
        u"\u0042": (u"\u0392", 66),
        u"\u0044": (u"\u0394", 68),
        u"\u0045": (u"\u0395", 69),
        u"\u0046": (u"\u03a6", 70),
        u"\u0047": (u"\u0393", 71),
        u"\u0048": (u"\u0397", 72),
        u"\u0049": (u"\u0399", 73),
        u"\u004a": (u"\u03d1", 74), 
        u"\u004b": (u"\u039a", 75),
        u"\u004c": (u"\u039b", 76),
        u"\u004d": (u"\u039c", 77),
        u"\u004e": (u"\u039d", 78),
        u"\u004f": (u"\u039f", 79),
        u"\u0050": (u"\u03a0", 80),
        u"\u0051": (u"\u0398", 81),
        u"\u0053": (u"\u03a3", 83),
        u"\u0054": (u"\u03a4", 84),
        u"\u0056": (u"\u03c2", 86),
        u"\u0057": (u"\u03a9", 87),
        u"\u0058": (u"\u039e", 88),
        u"\u0061": (u"\u03b1", 97),
        u"\u0062": (u"\u03b2", 98),
        u"\u0063": (u"\u03c7", 99),
        u"\u0064": (u"\u03b4", 100),
        u"\u0065": (u"\u03b5", 101),
        u"\u0066": (u"\u03c6", 102),
        u"\u0067": (u"\u03b3", 103),
        u"\u0068": (u"\u03b7", 104),
        u"\u0069": (u"\u03b9", 105),
        u"\u006a": (u"\u03c6", 106),
        u"\u006b": (u"\u03ba", 107),
        u"\u006c": (u"\u03bb", 108),
        u"\u006d": (u"\u03bc", 109),
        u"\u006e": (u"\u03bd", 110),
        u"\u006f": (u"\u03bf", 111),
        u"\u0070": (u"\u03c0", 112),
        u"\u0072": (u"\u03c1", 114),
        u"\u0073": (u"\u03c3", 115),
        u"\u0074": (u"\u03c4", 116),
        u"\u0075": (u"\u03c5", 117),
        u"\u0077": (u"\u03c9", 119),
        u"\u0079": (u"\u03c8", 121),
        u"\u007a": (u"\u03b6", 122),
        u"\u00a3": (u"\u1f10", 163),
        u"\u00c9": (u"\u03ae", 201),
        u"\u00d4": (u"\u1ff6", 212),
        u"\u00e1": (u"\u03ac", 225),
        u"\u00e2": (u"\u1fb6", 226),
        u"\u00e9": (u"\u03ad", 233),
        u"\u00ea": (u"\u1fc6", 234),
        u"\u00ec": (u"\u1f76", 236),
        u"\u00ed": (u"\u03af", 237),
        u"\u00f2": (u"\u1f78", 242),
        u"\u00f3": (u"\u03cc", 243),
        u"\u00fa": (u"\u03cd", 250),
        u"\u00fb": (u"\u1fe6", 251),
        u"\u00fc": (u"\u1f50", 252),
    },
    "Junicode": {
        u"006e": (u"n\u0364", 81),
        u"0077": (u"w\u0367", 90),
        u"007a": (u"z\u0364", 93),
        u"072b": (u"u\u0364", 2317),
        u"1e98": (u"w\u0366", 1243),
    },
    "OrigGarmndSo-Italic": {
     u"0053": (u"\u015a", 83),  
    },
    "OrigGarmndSo-Italic-SC750": { 
     u"004e": (u"\u0144", 78),   
    },
    "PSMT Special": { 
        u"": (u"\u0302", 26), # Hat das so seine Richtigkeit? Im Auge behalten!
    },
    "SGSonder2Italic": { # in der index.htm tw. ohne vorangestellte Buchstabengruppe gef�hrt - ok?
         u"\u0047": (u"\u011e", 71),
         u"\u0048": (u"\u1e2a", 72),
         u"\u0054": (u"\u1e6c", 84),  
         u"\u0055": (u"U\u0364", 85),
         u"\u0064": (u"\u1e0d", 100),  	
         u"\u006f": (u"o\u0367", 111),
         u"\u007a": (u"\u1e93", 122),  	
    },
    "SGSonder2Roman": {
         u"\u0055": (u"U\u0364", 85),
         u"\u0067": (u"g\u0305", 103),
         u"\u006d": (u"m\u0305", 109), # g mit K�rzungsstrich  
         u"\u006f": (u"o\u0367", 111), # m mit K�rzungsstrich
         u"\u00d2": (u"O\u0367", 210),
         u"\u00ea": (u"e\u0367", 234),
         u"\u00ef": (u"i\u0364", 239),     
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
        u"\u0056": (u"V\u0366", 86), 
        u"\u0067": (u"\u0121", 103),
        u"\u006b": (u"\u1e33", 107),
        u"\u00d8": (u"\u1e6c", 216),
    },
    "STGSneu-Roman": {
        u"\u0056": (u"V\u0366", 86),
        u"\u0068": (u"h\u032f", 104),
        u"\u00c4": (u"A\u0364", 196), 
        u"\u00d3": (u"O\u0367", 211),
        u"\u00e8": (u"e\u0367", 232), 
        u"\u00f2": (u"o\u036e", 242),
        u"\u00f3": (u"o\u0367", 243), 
    },
    "STGSneu2-Italic": {
        u"\u0061": (u"\u0101", 97),
        u"\u006f": (u"\u014d", 111),
        u"\u00eb": (u"e\u0366", 235),
    },
    "STGSneu2-Roman": {
        u"\u0045": (u"E\u0305", 69),
        u"\u0061": (u"a\u0305", 97),
        u"\u0069": (u"i\u0305", 105),
        u"\u006d": (u"m\u0305", 109), 
        u"\u006e": (u"n\u0305", 110),
        u"\u006f": (u"o\u0305", 111),
        u"\u0070": (u"p\u0305", 112),
        u"\u0072": (u"r\u0305", 114),
        u"\u0073": (u"s\u0305", 115),
        u"\u0074": (u"t\u0305", 116),
        u"\u00eb": (u"e\u0366", 235),   
    },
    "StGSonderBoldItalic": { 
        u"\u006e": (u"\u0148", 110),
        u"\u00a7": (u"\u015a", 167),
        u"\u00f7": (u"\u0159", 247),
        u"\u2021": (u"\u0142", 130),
    },
    "StGS4-Italic": {
        u"\u0043": (u"\u010c", 67),  
    },
    "StGS4-Roman": {
        u"\u00b0": (u"\u0366", 176), 
        u"\u00f2": (u"o\u0367", 242),
    },
     "StGSonderBold": {
        u"\u00fa": (u"u\u0366", 252), 
    },
    "StGSonderItalic": {
        u"\u0045": (u"\u0118", 69), 
        u"\u0047": (u"\u01e6", 71),
        u"\u0048": (u"\u1e24", 72), 
        u"\u0053": (u"\u1e62", 83),
        u"\u005a": (u"\u017d", 90),
        u"\u0065": (u"\u0119", 101),
        u"\u0067": (u"\u01e7", 103), 	
        u"\u0068": (u"\u1e25", 104),
        u"\u006e": (u"\u0148", 110),
        u"\u0074": (u"\u1e6d", 116),
        u"\u00a1": (u"\u017e", 161),
        u"\u00a2": (u"\u0107", 162),
        u"\u00a3": (u"\u011f", 163),  	
        u"\u00a7": (u"\u015a", 167),
        u"\u00a9": (u"\u0106", 169),
        u"\u00ae": (u"\u1e6f", 174), 
        u"\u00b5": (u"\u015b", 181),
        u"\u00ba": (u"\u015f", 186),
        u"\u00bf": (u"\u0121", 191),
        u"\u00d0": (u"\u0100", 208),   
        u"\u00d3": (u"\u01d1", 211),
        u"\u00d8": (u"\u0158", 216),
        u"\u00da": (u"U\u0366", 218),
        u"\u00df": (u"\u0143", 223),
        u"\u00e0": (u"\u01ce", 224),
        u"\u00e1": (u"\u0144", 225),
        u"\u00e2": (u"\u0103", 226), 
        u"\u00e3": (u"\u0101", 227),
        u"\u00e7": (u"\u010d", 231),
        u"\u00ea": (u"\u011b", 234),
        u"\u00eb": (u"\u0113", 235),  
        u"\u00ee": (u"\u012b", 238),
        u"\u00f0": (u"\u0161", 240),
        u"\u00f2": (u"o\u0364", 242), 
        u"\u00f4": (u"\u014f", 244), 
        u"\u00f5": (u"\u014d", 245), 
        u"\u00f6": (u"\u0151", 246), 
        u"\u00f7": (u"\u0159", 247),
        u"\u00f8": (u"\u1e63", 248),
        u"\u00f9": (u"u\u0364", 249),
        u"\u00fa": (u"u\u0366", 250),
        u"\u00fc": (u"\u016b", 252),
        u"\u0153": (u"\u1e2b", 156), 
        u"\u0160": (u"\u010c", 151),
        u"\u2021": (u"\u0142", 135), # aus BSB 2257. CID-Konflikt? 
        u"\u2021": (u"\u0142", 130), # aus BSB 2015. CID-Konflikt?
    },
    "StGSonderItalic-SC750": {
        u"\u00d8": (u"\u0158", 216),
    },
    "StGSonderRoman": {
        u"\u0045": (u"\u0118", 69),  
        u"\u0047": (u"\u01e6", 71), 
        u"\u0048": (u"\u1e24", 72),
        u"\u0050": (u"P\u0305", 80),
        u"\u0053": (u"\u1e62", 83),
        u"\u0063": (u"c\u0305", 99), 
        u"\u0065": (u"\u0119", 101),
        u"\u0068": (u"\u1e25", 104),
        u"\u0070": (u"p\u0305", 112), 
        u"\u0074": (u"\u1e6d", 116),
        u"\u00ae": (u"\u1e6f", 174),
        u"\u00ce": (u"v\u0366", 206),
        u"\u00d0": (u"A\u0305", 208), 
        u"\u00d3": (u"\u01d1", 211),
        u"\u00d8": (u"\u0158", 216),
        u"\u00da": (u"U\u0366", 218),
        u"\u00e3": (u"a\u0305", 227),
        u"\u00e4": (u"a\u0364", 228),
        u"\u00e8": (u"e\u0364", 232),
        u"\u00ea": (u"e\u011b", 234),
        u"\u00ee": (u"i\u0305", 238), # i mit langem K�rzungsstrich, konkurriert aus inhaltl. Gr�nden mit i mit macron (L�ngezeichen)
        u"\u00f2": (u"o\u0364", 242),
        u"\u00f3": (u"\u01d2", 243),
        u"\u00f5": (u"o\u0305", 245), # o mit langem K�rzungsstrich, konkurriert aus inhaltl. Gr�nden mit o mit macron (L�ngezeichen)
        u"\u00f7": (u"\u0159", 247),
        u"\u00f8": (u"\u1e63", 248),
        u"\u00f9": (u"u\u0364", 249),
        u"\u00fa": (u"u\u0366", 250),
        u"\u00fc": (u"u\u0305", 252), 
        u"\u2021": (u"\u0142", 130),
    },
    "StempelGaramondLTPro-Bold": {
        u"\u016f": (u"u\u0366", 31),
    },
    "StempelGaramondLTPro-Italic": {
        u"\u00e1": (u"\u00c1", 127),
        u"\u016f": (u"u\u0366", 31),
    },
    "StempelGaramondLTPro-Roman": {
        u"\u016e": (u"U\u0366", 10),
        u"\u016e": (u"U\u0366", 29), # aus BSB 2045
        u"\u016f": (u"u\u0366", 5), # aus BSB 2037
        u"\u016f": (u"u\u0366", 7), # aus BSB 2036
        u"\u016f": (u"u\u0366", 29),
        u"\u016f": (u"u\u0366", 31), # aus BSB 2045
    },
    "StempelGaramond-BoldItalic": {
        u"\u00b0":  (u"\u00ba", 176),# Ordnungszeichen m�nnlich 
    },
    "StempelGaramond-Italic": {
        u"\u00b0":  (u"\u00ba", 176),# Ordnungszeichen m�nnlich 
    },
    "StempelGaramond-Roman": {
        u"\u002b":  (u"\u205c", 43),# Ordnungszeichen m�nnlich 
        u"\u00b0":  (u"\u00ba", 176),# Ordnungszeichen m�nnlich 
    },
    "StempelGrmnd-Roman": {
        # u"\u00b0":  (u"\u0366", 176), (probehalber deaktiviert, da bisweilen Ordnungzeichen m�nnlich = U+00BA gemeint)
        u"\u00e5":  (u"a\u0366", 229),
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
        u"\u0041": (u"\u0391", 33),  # Alpha
        u"\u0047": (u"\u0393", 39),  # Gamma
        u"\u0048": (u"\u0397", 40),  # Eta
        u"\u0049": (u"\u0399", 41),  # Iota
        u"\u004b": (u"\u039a", 43),  # Kappa
        u"\u004c": (u"\u039b", 44),  # Lambda
        u"\u004d": (u"\u039c", 45),  # My
        u"\u0051": (u"\u0398", 52),  # Theta
        u"\u0051": (u"\u0398", 49),  # Theta
        u"\u0052": (u"\u03a1", 50),  # Rho
        u"\u0053": (u"\u03a3", 51),  # Sigma
        u"\u006a": (u"\u03c6", 74),  # phi
        u"\u0077": (u"\u03c9", 31),  # omega
        u"\u0398": (u"\u03a4", 52),  # Tau
    },
    "SymbolMT": {
        u"\u0021": (u"\u003e", 6), # Muss ich die Spitzklammer U+003e als &gt; codieren?
        u"\u0044": (u"\u0394", 39),
        u"\u0045": (u"\u0395", 40),
        u"\u0046": (u"\u03a6", 41),
        u"\u004f": (u"\u039f", 50),
        u"\u0051": (u"\u0398", 52), 
        u"\u0057": (u"\u03a9", 58),
        u"\u00a2": (u"\u2329", 3), 
        u"\u00b2": (u"\u232a", 2),
    },
    "TimesNewRomanPS-ItalicMT": {
        u"\u0092": (u"\u2019", 2), # Platzhalterzeichen zu einf. Anf.zeichen rechts. Zu speziell?
        u"\u00b0": (u"\u00ba", 74), # Gradzeichen zu Ordnungszeichen m�nnlich. Zu speziell? 
        u"\u0131": (u"\u00ed", 213), 
        u"\u016f": (u"u\u0366", 292),
        u"\u02db": (u"\u0105", 222), 
    },
    "TimesNewRomanPSMT": {
        # u"\u0065": (u"\u0119", 101), Aus BSB 2037; macht aber z.B. in BSB 2246 Probleme
        # u"\u00b0": (u"y\u0366", 176), Aus BSB 2016; macht aber z.B. in BSB 2246 Probleme 
        u"\u00b0": (u"\u00ba", 176), # Ordnungszeichen m�nnlich
        u"\u016e": (u"U\u0366", 291), # Ersetzung: U mit Ring > U mit �bergeschr. o
        u"\u016f": (u"u\u0366", 157), # Ersetzung: u mit Ring > u mit �bergeschr. o. Dopplung mit CID 292
        u"\u016f": (u"u\u0366", 292), # Ersetzung: u mit Ring > u mit �bergeschr. o. Dopplung mit CID 157
    },
    "Timespunktiert": {
        u"\u0043": (u"C\u0323", 67),
        u"\u0049": (u"I\u0323", 73),
        u"\u004c": (u"L\u0323", 76),
        u"\u0061": (u"a\u0323", 97),
        u"\u0065": (u"e\u0323", 101),
        u"\u0068": (u"h\u0323", 104),
        u"\u0069": (u"i\u0323", 105),
        u"\u006d": (u"m\u0323", 109),
        u"\u006e": (u"n\u0323", 110),
        u"\u0072": (u"r\u0323", 114),
        u"\u0073": (u"s\u0323", 115),
        u"\u0074": (u"t\u0323", 116),
        u"\u0075": (u"u\u0323", 117),
    },
    "Timespunktiert-Bold": {
        u"\u006e": (u"n\u0323", 110),
    },
    "TimesSonder-Italic": {
        u"\u0023": (u"\u0158", 35), 
        u"\u0047": (u"\u01e6", 71),
        u"\u0048": (u"\u1e24", 72), 
        u"\u0053": (u"\u1e62", 83),
        u"\u0063": (u"\u0107", 99),
        u"\u0064": (u"\u1e0f", 100), 
        u"\u0065": (u"\u0119", 101),
        u"\u0067": (u"\u01e7", 103), 
        u"\u0068": (u"\u1e25", 104),
        u"\u0069": (u"\u012b", 105),
        u"\u006c": (u"\u0142", 108),
        u"\u006e": (u"\u0144", 110),
        u"\u0072": (u"\u0159", 114),
        # u"\u0073": (u"\u1e6e", 115), Versehen oder tats�chlich gro�es T mit Unterstrich? 
        u"\u0073": (u"\u1e63", 115),
        u"\u0074": (u"\u1e6d", 116),
        u"\u007a": (u"\u017e", 122), 
        u"\u00a2": (u"\u0121", 162), 
        u"\u00a4": (u"\u015b", 130),
        u"\u00aa": (u"\u015f", 170),
        u"\u00b1": (u"\u1e6e", 177),
        u"\u00bf": (u"\u1e2b", 191),
        u"\u00c3": (u"\u0100", 195),
        u"\u00c4": (u"\u0120", 196),
        u"\u00c7": (u"\u011e", 199),
        u"\u00e0": (u"\u0101", 224), 
        u"\u00e6": (u"\u011b", 230),
        # u"\u00f3": (u"\u014f", 243),  W�rde in eine verkettete Transformation f�hren
        u"\u00f6": (u"o\u0364", 246),
        u"\u00f7": (u"\u010c", 247),
        u"\u00fa": (u"u\u0366", 250),
        u"\u00fb": (u"\u016b", 251),
        u"\u00fd": (u"\u1e2a", 253),
        u"\u00fe": (u"\u011f", 254),
        # u"\u014f": (u"u\u014d", 243), W�re 2. Glied einer verketteten Transformation
        u"\u0152": (u"u\u0364", 140),
        u"\u0160": (u"\u015a", 138),
        u"\u0161": (u"\u010d", 154), # BSB 2020, 2031, 2929, 2258
        u"\u0161": (u"\u010d", 157), # BSB 2033
        u"\u0192": (u"\u1e6f", 134), 
        u"\u201d": (u"\u0148", 148),
        u"\u2020": (u"\u1e0d", 129),
    },
     "TimesSonder-Italic-SC750": {
        u"\u0063": (u"\u0107", 67),
    },
    "TimesSonder-Roman": {
        u"\u003e": (u"V\u0302", 62), 
        u"\u0045": (u"\u0118", 69),
        u"\u0047": (u"\u01e6", 71),
        u"\u0048": (u"\u1e24", 72),
        u"\u0052": (u"R\u0305", 82),
        u"\u0053": (u"\u1e62", 83),
        u"\u0056": (u"V\u0366", 86), # ge�ndert aus V + Kringel (=u030a)
        u"\u0062": (u"\u1e07", 98),
        u"\u0064": (u"\u1e05", 100),  
        u"\u0058": (u"\u25b2", -1),
        u"\u005a": (u"\u017d", 90),
        u"\u0063": (u"\u0107", 99),
        u"\u0065": (u"\u0119", 101),
        u"\u0067": (u"\u01e7", 103),
        u"\u0068": (u"\u1e25", 104),
        u"\u0069": (u"\u012b", 1),
        u"\u0069": (u"\u012b", 105),
        u"\u006c": (u"\u0142", 108),
        u"\u006d": (u"m\u0304", 2),
        u"\u006d": (u"m\u0304", 109),
        u"\u006e": (u"\u0144", 110),
        u"\u006f": (u"\u0131\u0366", 111),
        u"\u0072": (u"\u0159", 114),
        u"\u0073": (u"\u1e63", 115),
        u"\u0074": (u"t\u0323", 116), 
        u"\u0075": (u"u\u0364", 117),
        u"\u0076": (u"v\u0366", 118),
        u"\u0077": (u"w\u0364", 119),
        u"\u0078": (u"\u25b2", 120),
        u"\u0079": (u"v\u0302", 121),  # older context had: u"\u0079": (u"\u0177", 121),
        u"\u007a": (u"\u017e", 122),
        u"\u007d": (u"v\u0364", 125),
        u"\u00a1": (u"l\u0304", 161),
        u"\u00a3": (u"n\u0304", 163), 
        u"\u00a9": (u"W\u0366", 169),
        u"\u00ae": (u"c\u0304", 174),
        u"\u00b3": (u"e\u0323", 179), # ge�ndert aus hart codiertem e mit Unterpunkt U+01B9
        u"\u00bf": (u"\u1e2b", 191), 
        u"\u00c3": (u"\u0100", 195),
        u"\u00c4": (u"\u0120", 196),
        u"\u00c7": (u"c\u011e", 199), 
        u"\u00d2": (u"O\u036e", 210), # ge�ndert aus O mit Caron
        u"\u00d3": (u"O\u0364", 211),
        u"\u00d4": (u"\u01d1", -1),
        u"\u00d5": (u"O\u0305", 213),
        u"\u00da": (u"\u016e", -1),
        # u"\u00e0": (u"a\u0364", -1), 
        u"\u00e0": (u"\u0101", 3),
        u"\u00e0": (u"\u0101", 224),
        u"\u00e2": (u"\u01ce", 226),
        u"\u00e5": (u"a\u0323", 229),
        u"\u00e6": (u"\u011b", 230),
        u"\u00e8": (u"\u0113", 232),
        u"\u00ed": (u"i\u0364", -1),
        u"\u00ee": (u"\u01d0", 238),
        u"\u00f0": (u"r\u0364", -1),
        u"\u00f2": (u"o\u036e", 242),
        u"\u00f3": (u"\u014d", 243), 
        u"\u00f4": (u"\u01d2", -1),
        u"\u00f6": (u"o\u0364", 246),
        u"\u00f7": (u"\u010c", 247),
        u"\u00fa": (u"u\u0366", 250),
        u"\u00fb": (u"\u016b", 4), 
        u"\u00fb": (u"\u016b", 251),
        u"\u00fd": (u"\u01e2a", 253),
        u"\u00ff": (u"g\u0304", 255),
        u"\u0131": (u"i\u0366", 7),
        u"\u0152": (u"u\u0364", 140),
        u"\u0161": (u"\u010d", 154),    
        u"\u0161": (u"\u010d", 157),    
        u"\u0178": (u"i\u0323", 159),
        u"\u0192": (u"\u1e6f", 131),
        u"\u2020": (u"d\u0323", 134),  
        u"\u2122": (u"i\u036e", 146),  # (i with caron (U+01D0)?)
    },
    "TimesSonder2": {
        u"\u0061": (u"\u0363", 97),
        u"\u00b0": (u"\u030a", 176),
    },
    "TimesSonder3": {
        u"\u002b": (u"t\u0304", 43), 
        u"\u003e": (u"V\u0302", 62),
        u"\u0054": (u"\u1e6c", 84),
        u"\u0056": (u"V\u0366", 86),
        u"\u0064": (u"d\u0364", 100),
        u"\u0065": (u"e\u0363", 101), 
        u"\u0066": (u"f\u0364", 102),
        u"\u0067": (u"g\u0364", 103),
        u"\u0068": (u"h\u0364", 104),
        u"\u006d": (u"m\u0364", 109),
        u"\u006f": (u"o\u0323", 111), 
        u"\u0070": (u"p\u0364", 112),
        u"\u0072": (u"r\u0366", 114),
        u"\u0073": (u"s\u0364", 115),
        u"\u0074": (u"t\u0364", 116),
        u"\u0075": (u"u\u0364", 117),
        u"\u0076": (u"v\u0364", 118),
        u"\u0077": (u"w\u0367", 119),
        # u"\u0079": (u"v\u030a", 121), CID-Konflikt
        # u"\u0079": (u"y\u0366", 121), CID-Konflikt (hier nach BSB 2025)
        u"\u007a": (u"z\u0364", 122),
        u"\u007b": (u"r\u0323", 123),
        u"\u007d": (u"w\u0366", 125),
        # u"\u007d": (u"v\u0364", 125),
        u"\u00a2": (u"g\u0323", 162),
        u"\u00a9": (u"W\u0366", 169),
        u"\u00b0": (u"a\u1de0", 176),
        u"\u00b2": (u"v\u0364", 178),
        u"\u00b3": (u"\u1eb9", 179),
        u"\u00b9": (u"v\u0365", 185),
        u"\u00bb": (u"w\u036e", 187),
        u"\u00bc": (u"v\u0302", 188),
        u"\u00c0": (u"A\u0364", 192),
        u"\u00c2": (u"A\u0367", 194),   
        u"\u00c8": (u"E\u0367", 200),
        u"\u00d0": (u"\u017c", 208),
        u"\u00d2": (u"O\u0367", 210),
        u"\u00d3": (u"O\u0364", 211),
        u"\u00d7": (u"u\u0365", 215),
        u"\u00da": (u"U\u0366", 218),
        u"\u00dc": (u"U\u0364", 220),
        u"\u00e0": (u"a\u0364", 224),
        u"\u00e1": (u"a\u0366", 225),
        u"\u00e2": (u"a\u0367", 226),
        u"\u00e3": (u"a\u0365", 227),
        u"\u00e4": (u"a\u036e", 228),
        u"\u00e8": (u"e\u036e", 232),
        u"\u00eb": (u"e\u0364", 235),
        u"\u00ed": (u"i\u0364", 237),
        u"\u00f0": (u"r\u0364", 240),
        u"\u00f1": (u"n\u0364", 241),
        u"\u00f2": (u"o\u0366", 242),
        u"\u00f3": (u"o\u0367", 243),
        u"\u00f4": (u"\u01d2", 244),
        u"\u00f5": (u"o\u0365", 245),
        u"\u00f6": (u"o\u0364", 246),
        u"\u00f9": (u"u\u0367", 249),
        u"\u00fb": (u"u\u036e", 251),
        u"\u00fc": (u"u\u0323", 252),  
        u"\u00fd": (u"y\u0364", 253),
        u"\u0152": (u"u\u0364", -1),
        u"\u0178": (u"i\u0323", 159),
        u"\u2022": (u"u\u0365", 244),
        u"\u2030": (u"r\u0365", 137),
    },
    "TimesSonder3-Italic": {
        u"\u0052": (u"\u0158", 82),
        u"\u0054": (u"\u1e6c", 84),
        u"\u005a": (u"\u017b", 90),
        u"\u00a4": (u"\u0161", 130),
        u"\u00d0": (u"\u017c", 208),
        u"\u00e0": (u"a\u0364", 224),
        u"\u00e5": (u"\u0105", 229),
        u"\u00e6": (u"\u011b", 230),
        u"\u00f7": (u"\u010c", 247),
        u"\u014f": (u"\u014d", 243),
        u"\u201d": (u"\u0148", 148),
    },
    "TimesSonder4": {
        u"\u00f9": (u"u\u0365", 5),
    },
    "TT Special": { 
        u"\u0023": (u"\u0042", 35),
        # u"\u0028": (u"\u1F7B5", 40), F�hrt zu fehlerhafter Ersetzung von (
        # u"\u002b": (u"\u2329", 43), F�hrt zu fehlerhafter Ersetzung von +
        # u"\u002c": (u"\u232a", 44), F�hrt zu fehlerhafter Ersetzung von ,
        # u"\u0045": (u"\u00ba", 69), F�hrt zu fehlerhafter Ersetzung von E
        # u"\u0047": (u"\u01e6", 71), F�hrt zu fehlerhafter Ersetzung von G
        # u"\u0048": (u"\u1e24", 72), F�hrt zu fehlerhafter Ersetzung von H
        # u"\u0053": (u"\u015a", 83), F�hrt zu fehlerhafter Ersetzung von S
        # u"\u0054": (u"\u1e6c", 84), F�hrt zu fehlerhafter Ersetzung von T
        # u"\u0065": (u"\u0119", 101), F�hrt zu fehlerhafter Ersetzung von e
        # u"\u0067": (u"\u01e7", 103), F�hrt zu fehlerhafter Ersetzung von g
        # u"\u0068": (u"\u1e25", 104), F�hrt zu fehlerhafter Ersetzung von h
        # u"\u0069": (u"\u012b", 105), F�hrt zu fehlerhafter Ersetzung von i
        # u"\u006c": (u"\u0142", 108), F�hrt zu fehlerhafter Ersetzung von l
        # u"\u0072": (u"\u0159", 114), F�hrt zu fehlerhafter Ersetzung von r
        # u"\u0073": (u"\u1e63", 115), F�hrt zu fehlerhafter Ersetzung von s
        # u"\u0074": (u"\u1e6d", 116), F�hrt zu fehlerhafter Ersetzung von t
        # u"\u0076": (u"v\u0364", 118), F�hrt zu fehlerhafter Ersetzung von v
        # u"\u0077": (u"w\u0364", 119), F�hrt zu fehlerhafter Ersetzung von w
        u"\u00a2": (u"\u0121", 162),
        u"\u00a6": (u"\u00a0", 166),
        u"\u00b0": (u"\u00ba", 74),
        u"\u00bb": (u"\u0142", 187),
        # u"\u00c4": (u"\u0120", 196), F�hrt zu fehlerhafter Ersetzung von �
        u"\u00d0": (u"\u015a", 208),
        # u"\u00d6": (u"O\u0364", 214), F�hrt zu fehlerhafter Ersetzung von �
        # u"\u00e0": (u"\u0105", 224), F�hrt zu fehlerhafter Ersetzung von �
        # u"\u00e2": (u"\u0101", 226), F�hrt zu fehlerhafter Ersetzung von �
        # u"\u00e4": (u"a\u0364", 228), F�hrt zu fehlerhafter Ersetzung von �
        u"\u00eb": (u"e\u0364", 235),
        # u"\u00f4": (u"o\u036e", 244), F�hrt zu fehlerhafter Ersetzung von �
        # u"\u00f6": (u"o\u0364", 246), F�hrt zu fehlerhafter Ersetzung von �
        # u"\u00fb": (u"u\u036e", 251), F�hrt zu fehlerhafter Ersetzung von �
        # u"\u00fc": (u"u\u0364", 252), F�hrt zu fehlerhafter Ersetzung von �
        u"\u00fd": (u"\u1e2a", 253),
        u"\u0105": (u"\u0101", 224),
        u"\u0192": (u"\u1e6f", 134),
        # u"\u201c": (u"\u0119", 141), F�hrt zu fehlerhafter Ersetzung von �
        # u"\u2020": (u"\u1e0d", 129), F�hrt zu fehlerhafter Ersetzung von �
    },
    "Wingdings2": {
        u"\u00cb": (u"\u2020", 173),
    },
    "WP-MathA": { 
        u"\u0045": (u"\u00ba", 69),
        u"\uf069": (u"\u2300", 76), # Ausgangszeichen liegt in der Private Use Area
    },
}


class BaseCorrector(FontCorrector):

    def __init__(self):
        pass

    def correct(self, font):
        self.adjust_font_metrics(font)
        self.reencode_font(font)

    def reencode_font(self, font):
        # first, go for a lucky guess
        basefontname = self._mk_basename(font.fontname)
        swaptable = swaptables.get(basefontname)
        if swaptable is not None:
            self.reencode(font, swaptable)
        elif self._is_tt_font(font.fontname):
            self.reencode(font, swaptables["TT Special"])
        elif "TimesSonder2" in font.fontname:
            self.reencode(font, swaptables["TimesSonder2"])
        elif "TimesSonder3" in font.fontname:
            self.reencode(font, swaptables["TimesSonder3"])
        elif "TimesSonder" in font.fontname:
            self.reencode(font, swaptables["TimesSonder-Roman"])
        elif "GriechischMedium" in font.fontname:
            self.reencode(font, swaptables["GriechischMedium"])
        elif "Spezialzeichen" in font.fontname:
            self.reencode(font, swaptables["Spezialzeichen"])
        elif self._is_psmt_font(font.fontname):
            self.cid_reencode(font, swaptables["PSMT Special"])
        elif self._is_symbol_font(font.fontname):
            try:
                self.reencode(font, swaptables["Symbol"])
            except FontCorrectorError:
                logging.warning("Trying CID update.")
                self.cid_reencode(font, swaptables["Symbol"])
    
    def _mk_basename(self, fontname):
        pos = fontname.find("+")
        if pos == -1:
            return fontname
        return fontname[pos + 1:]

    def adjust_font_metrics(self, font):
        if self._is_tt_font(font.fontname):
            font.descriptor[u"FontBBox"] = [-198, -247, 1213, 1013]
            font.bbox = font.descriptor[u"FontBBox"]
            font.descriptor[u"Descent"] = -216
            font.descent = font.descriptor[u"Descent"]
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
                ctu[k] = swap.get(v, (v, None))[0]
            font.cid2unicode = ctu
            if font.unicode_map:
                font.unicode_map.cid2unichr.update(ctu)
        except AttributeError:
            msg = "Cannot directly re-encode font %s. Trying cid_reencode."
            logging.warning(msg, font.fontname)
            self.cid_reencode(font, swap)

    def cid_reencode(self, font, swap):
        swap = self._recode_swap_table(swap)
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
                logging.warning("Could not re-encode font {}. Building ad-hoc unicode_map."\
                        .format(font.fontname))
                unicode_map = FileUnicodeMap()
                unicode_map.cid2unichr.update(swap)
                font.unicode_map = unicode_map

    def _recode_swap_table(self, swap):
        """
        Re-arrange the swap table.

        Input looks like: {instr: (outstr, cid),}

        Output should look like: {cid: outstr}
        """
        ret = {}
        for k in swap:
            ret[swap[k][1]] = swap[k][0]
        return ret
