# -*- coding: UTF-8 -*-

"""
anapdf
"""

import argparse
import logging

import anapdf

def main():
    """Open PDF files and extract some analytical information"""
    description = "Open PDF files and extract some analytical information"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
            "pdffile",
            metavar="PDFFILE",
            type=str,
            help=u"the PDF file to analyze")
    parser.add_argument(
            "-d",
            "--debug",
            help=u"log some debugging information",
            default=False,
            action="store_true",
            dest="b_debug")
    parser.add_argument(
            "-i",
            "--images",
            help=u"directory where images will be stored",
            default="imdir",
            type=str,
            dest="imdir",
            metavar="IMAGEDIR")
    parser.add_argument(
            "-f",
            "--fontdir",
            help=u"directory where font information will be stored",
            default="fonts",
            type=str,
            dest="fontdir",
            metavar="FONTDIR")
    parser.add_argument(
            "-r",
            "--res",
            "--resolution",
            help=u"resolution of created images in dpi (defaults to 300)",
            default=300,
            type=int,
            dest="resolution",
            metavar="RESOLUTION")
    parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s {version}".format(version=anapdf.__version__))
    parser.add_argument(
            "-s",
            "--skip-images",
            help=u"skip image creation",
            default=True,
            action="store_false",
            dest="make_images")
    parser.add_argument(
            "-x",
            "--no-xml",
            "--noxml",
            help=u"skip xml extraction",
            default=True,
            action="store_false",
            dest="extract_xml_data")
    parser.add_argument(
            "--no-fonts",
            "--nofonts",
            help=(u"skip font extraction (index.htm)"),
            default=True,
            action="store_false",
            dest="extract_fonts")
    )
    parser.add_argument(
            "-c",
            "--corr",
            "--corrector",
            help=u"filename of module containing FontCorrector loader",
            default=None,
            dest="font_corrector_filename",
            metavar="FC_CORRECTOR_LOADER")
    parser.add_argument(
            "-o",
            "--outfile",
            help=(u"store XML output in this file "
                  u"(defaults to PDFFILE with xml extension)"),
            dest="outfilename",
            metavar="OUTFILE"
    )
    parser.add_argument(
            "--horz",
            help=u"horizontal scaling character bbox (percent)",
            default=100.0,
            type=float,
            dest="horz")
    parser.add_argument(
            "--vert",
            help=u"vertical scaling character bbox (percent)",
            default=100.0,
            type=float,
            dest="vert")
    args = parser.parse_args()
    if args.b_debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    if args.font_corrector_filename:
        import imp
        fc_loader = imp.load_source("fc_loader", args.font_corrector_filename)
        font_correctors = fc_loader.fc_loader()
        args = vars(args)
        args["font_correctors"] = font_correctors
    else:
        args = vars(args)
    args["scales"] = (args["horz"], args["vert"])
    a = anapdf.Analyzer(**args)
    a.analyze()

if __name__ == "__main__":
    main()
