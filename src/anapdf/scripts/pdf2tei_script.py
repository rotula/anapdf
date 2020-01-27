# -*- coding: UTF-8 -*-

"""
pdf2tei

Convert PDF file to TEI.

If an XML file is given, it is supposed to be a resulting file from
PDFMiner's ``pdf2txt.py``.
"""

import sys
import os.path
import argparse
import logging

from lxml import etree as et

import anapdf

def main():
    """Open PDF files and extract some analytical information"""
    description = "Convert PDF file to TEI XML."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "pdffile",
        metavar="PDFFILE",
        type=str,
        help=u"the PDF file to analyze (or the XML resulting "
        u"from a PDFMiner run)"
    )
    parser.add_argument(
        "-f",
        "--font",
        "--fontencfile",
        help=u"font re-encoding file (usually ``index.htm`` resulting "
        u"from an ``anapdf`` run), if none is given, the "
        u"characters will remain the same as in the PDF/XML",
        default="",
        type=str,
        dest="fontencfile",
        metavar="FONTENCODINGFILE"
    )
    parser.add_argument(
        "-o",
        "--output",
        help=u"if none given, append ``_tei`` to filename, "
        u"if ``-``, print to stdout",
        default="",
        type=str,
        dest="output",
        metavar="OUTPUTFILE"
    )
    parser.add_argument(
        "-s",
        "--stop",
        help=u"Stop after given number of pages (for debugging purposes)",
        default=None,
        dest="stop_after",
        type=int,
        metavar="STOPAFTER"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=anapdf.__version__)
    )
    parser.add_argument(
        "-c",
        "--corr",
        "--corrector",
        help=u"filename of module containing FontCorrector loader",
        default=None,
        dest="font_corrector_filename",
        metavar="FC_CORRECTOR_LOADER"
    )
    parser.add_argument(
        "-l",
        "--logging",
        help=u"turn on more logging (INFO instead of WARNING)",
        default=False,
        dest="b_logging",
        action="store_true"
    )
    parser.add_argument(
        "-b",
        "--basesize",
        "--basefontsize",
        help=u"assume a default base font size",
        default="0.0",
        dest="basesize",
        type=float,
        metavar="BASESIZE"
    )
    args = parser.parse_args()
    if args.b_logging:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    font_correctors = []
    if args.font_corrector_filename:
        import imp
        fc_loader = imp.load_source("fc_loader", args.font_corrector_filename)
        font_correctors = fc_loader.fc_loader()
    if args.basesize != 0.0:
        basesize = args.basesize
    else:
        basesize = None
    conv = anapdf.TEIConverter(
        args.pdffile,
        fontencfile=args.fontencfile,
        font_correctors=font_correctors,
        default_font_size=basesize
    )
    conv.convert(args.stop_after)
    if args.output == "-":
        outfile = sys.stdout
    else:
        if args.output == "":
            outfilename = os.path.splitext(args.pdffile)[0] + "_tei.xml"
        else:
            outfilename = args.output
        outfile = open(outfilename, "wb")
    conv.write(outfile)
    if args.output != "-":
        outfile.close()

if __name__ == "__main__":
    main()
