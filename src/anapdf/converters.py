#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Converter for PDF files
"""

import os.path
import logging
import io

from lxml import etree as et
from lxml.builder import ElementMaker
import xmlhelper
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from simplestyle import styles

from . import fontenc

ns = xmlhelper.ns
tei = ns["tei"]
xmlns = ns["xml"]
T = ElementMaker(namespace=tei, nsmap={None: tei})

class ConverterError(Exception): pass

class Converter(object):
    """Base class for all PDF converters"""

    sourcefile = ""

    def convert(self):
        """Do the conversion"""
        raise NotImplementedError

    def write(self, destination):
        """Write to destination"""
        raise NotImplementedError

class TEIConverter(Converter):
    """Converts a PDF file to TEI XML"""

    sourcefile = None
    doc = None  # the XML file
    teidoc = None
    repltable = None  # font re-encoding table
    current_size = 0.0  # while processing line, current default size
    current_base = 0.0  # while processing line, current default base
    styles = None  # dictionary of styles
    next_style = 1
    facs_coor = None  # facsimile for coordinates
    facs_scan = None  # facsimile for scans
    pagecount = 0  # current page
    textboxcount = 0  # current textbox
    linecounter = 0  # current line on page
    wordcount = 0  # current word in line
    font_correctors = None  # list of font correctors
    default_font_size = None  # a base font size to be assumed
    g_list = None  # a list of all glyph elements, they need
                   # some preprocessing

    replace_soft_hyphen = True  # Always replace soft hyphens with hard
                                  # hyphens.

    MIXED = 0  # mixed wordsize: at least two different sizes detected
    CLEAN = 1  # clean wordsize: every letter of same size

    schematron_rules = "<?xml-model href=\"http://www.tei-c.org/"\
            "release/xml/tei/custom/schema/relaxng/tei_all.rng\" "\
            "type=\"application/xml\" schematypens=\"http://relaxng"\
            ".org/ns/structure/1.0\"?>\n"\
            "<?xml-model href=\"http://www.tei-c.org/release/xml/"\
            "tei/custom/schema/relaxng/tei_all.rng\" type=\""\
            "application/xml\" schematypens=\"http://purl.oclc."\
            "org/dsdl/schematron\"?>"

    def __init__(self, sourcefile, fontencfile=None, font_correctors=None,
                 default_font_size=None, replace_soft_hyphen=True):
        if not os.path.isfile(sourcefile):
            raise ConverterError("File not found: {}".format(str(sourcefile)))
        if sourcefile.endswith(".xml"):
            self.g_list = []
            context = et.iterparse(sourcefile, tag=["g", "pages"])
            for _, element in context:
                if element.tag == "g":
                    self.g_list.append(element)
            self.doc = element.getroottree()
        elif sourcefile.endswith(".pdf"):
            self.doc = et.fromstring(self._get_xml_data(sourcefile))\
                    .getroottree()
        else:
            raise ConverterError("{} appears to be neither XML nor PDF."\
                    .format(str(sourcefile)))
        if self.g_list is None:
            self.g_list = []
            for g in self.doc.iter("g"):
                self.g_list.append(g)
        self.sourcefile = sourcefile
        if fontencfile:
            if not os.path.isfile(fontencfile):
                raise ConverterError("Font re-encoding file {} not found."\
                        .format(str(fontencfile)))
            self.repltable = fontenc.read(fontencfile)
        self.font_correctors = []
        if font_correctors is not None:
            for fc in font_correctors:
                self.font_correctors.append(fc)
        self.styles = {}
        self.default_font_size = default_font_size
        self.replace_soft_hyphen = replace_soft_hyphen

    def add_style(self, style):
        """Add a style to the dictionary, return style id."""
        styleid = None
        for si, s in list(self.styles.items()):
            if s == style:
                styleid = si
                break
        if styleid is None:
            styleid = "style_{}".format(self.next_style)
            self.next_style += 1
            self.styles[styleid] = style
        return styleid

    def get_surface_coor(self, e):
        """Get coordinates of surface element"""
        ret = {}
        bbox = e.get("bbox")
        if bbox is None:
            return ret
        coords = bbox.split(",")
        ret["ulx"] = coords[0]
        ret["uly"] = coords[3]
        ret["lrx"] = coords[2]
        ret["lry"] = coords[1]
        return ret

    def convert(self, stop_after=None):
        """Create the TEI file
        
        Args:
            stop_after(int): stop after n pages, leave empty to process all
        """
        # @@@Experimental: preflight for special characters
        # (<g>)
        self._handle_glyphs()
        body = self.doc.getroot()
        body.tag = "{{{}}}body".format(tei)
        tei_header = self.make_tei_header()
        self.teidoc = T.TEI()
        self.teidoc.text = "\n"
        self.teidoc.append(tei_header)
        self.facs_coor = T.facsimile(ana="#facsCoor")
        self.facs_coor.text = "\n "
        self.facs_coor.tail = "\n"
        self.facs_scan = T.facsimile(ana="#facsScan")
        self.facs_scan.text = "\n "
        self.facs_scan.tail = "\n"
        self.teidoc.append(self.facs_scan)
        self.teidoc.append(self.facs_coor)
        text = T.text()
        text.text = "\n"
        text.tail = "\n"
        self.teidoc.append(text)
        text.append(body)
        self.pagecount = 0
        for page in self.doc.xpath("//page"):
            self.pagecount += 1
            # stopping?
            if isinstance(stop_after, int):
                if stop_after > 0:
                    if self.pagecount > stop_after:
                        xmlhelper.delete(page)
                        continue
            self.current_page_surface = T.surface(
                    "\n  ",
                    self.get_surface_coor(page),
                    sameAs="#page_{:05d}".format(self.pagecount))
            self.current_page_surface.tail = "\n "
            self.facs_coor.append(self.current_page_surface)
            self.deal_with_page(page)
            page.tag = "{{{}}}div".format(tei)
            page.set("type", "page")
            surface = T.surface(
                    "\n  ",
                    {"{{{}}}id".format(xmlns):
                        "page_{:05d}".format(self.pagecount),},
                    T.desc(
                        "\n   ",
                        T.list(
                            "\n    ",
                            T.label(ana="#sequenceNo"),
                            T.item(str(page.get("id"))),
                            "\n   ",
                            ana="#mgh_ident"),
                        "\n  "),
                    "\n ")
            surface.tail = "\n "
            label = page.get("label")
            if label:
                surface[0][0][-1].tail = "\n    "
                surface[0][0].append(T.label(ana="#nativeNo"))
                surface[0][0].append(T.item(label))
                surface[0][0][-1].tail = "\n  "
                page.set("n", label)
            self.facs_scan.append(surface)
            page.set("sameAs", "#page_{:05d}".format(self.pagecount))
            xmlhelper.delat(page, "id")
            xmlhelper.delat(page, "rotate")
            xmlhelper.delat(page, "bbox")
            xmlhelper.delat(page, "label")
            xmlhelper.delat(page, "cropbox")
            xmlhelper.delat(page, "cropboxraw")
            # correct indentation
            try:
                self.current_page_surface[-1].tail = "\n "
            except IndexError:
                pass
        # correct indentation
        try:
            self.facs_scan[-1].tail = "\n"
        except IndexError:
            pass
        try:
            self.facs_coor[-1].tail = "\n"
        except IndexError:
            pass
        # now add styles
        td = self.teidoc.xpath("//tei:tagsDecl", namespaces=ns)[0]
        for styleid, style in list(self.styles.items()):
            rendition = T.rendition({
                "{{{}}}id".format(xmlns): styleid,})
            rendition.tail = "\n"
            rendition.text = style.get_css()
            td.append(rendition)
        # try to cleanup namespaces
        et.cleanup_namespaces(self.teidoc)
        return

    def _handle_glyphs(self):
        for g in self.g_list:
            text = g.getparent()
            txt = self._get_text_content(text)
            text.text = txt
        for g in self.g_list:
            xmlhelper.delete(g)

    def deal_with_page(self, page):
        """Convert a single page"""
        # For the time being we only ever use the textboxes,
        # convert them to tei:divs and discard everything else
        # (rects, layout).
        self.linecounter = 0
        self.textboxcount = 0
        for e in page:
            if e.tag == "textbox":
                self.deal_with_textbox(e)
            else:
                xmlhelper.delete(e)

    def deal_with_textbox(self, textbox):
        """Convert textbox to div"""
        textbox.tag = "{{{}}}div".format(tei)
        textbox.set("type", "textbox")
        self.textboxcount += 1
        textboxid = "tb_{:05d}_{:03d}".format(self.pagecount, self.textboxcount)
        tbcoord = self.get_surface_coor(textbox)
        tbcoord["{{{}}}id".format(xmlns)] = textboxid
        zone = T.zone(
                tbcoord,
                )
        zone.tail = "\n  "
        self.current_page_surface.append(zone)
        xmlhelper.delat(textbox, "bbox")
        # textbox.set("n", textbox.get("id"))
        xmlhelper.delat(textbox, "id")
        textbox.set("sameAs", "#" + textboxid)
        self.linecounter = 0
        for e in textbox:
            if e.tag == "textline":
                self.linecounter += 1
                self.deal_with_textline(e)
                lineid = "line_{:05d}_{:03d}_{:03d}".format(
                        self.pagecount, self.textboxcount, self.linecounter)
                e.tag = "{{{}}}l".format(tei)
                e.set("sameAs", "#" + lineid)
                linecoord = self.get_surface_coor(e)
                linecoord["{{{}}}id".format(xmlns)] = lineid
                zone = T.zone(linecoord)
                zone.tail = "\n  "
                self.current_page_surface.append(zone)
                xmlhelper.delat(e, "bbox")
            else:
                print(("Unexpected element {} in textbox".format(e.tag)))

    def _create_seg(self, segtype=None):
        """Helper to create a generic segment element"""
        ret = T.seg()
        if segtype:
            ret.set("type", segtype)
        ret.tail = "\n"
        ret.text = "\n"
        return ret

    def _get_text_content(self, text):
        ret = []
        ret.append((text.text or u""))
        for child in text:
            if child.tag == "g":
                value = child.get("value")
                try:
                    value = int(value)
                except:
                    print((u"Value '{}' not supported, must be integer."\
                        .format(value)))
                if value == 0:
                    ret.append(u" ")
                elif value == 9:
                    ret.append(u" ")
                else:
                    print((u"Unsupported control character (<g value='{}'>)".format(value)))
            else:
                print((u"Unexpected element {}".format(child.tag)))
            ret.append((child.tail or u""))
        return "".join(ret)

    def deal_with_textline(self, textline):
        """Convert a line"""
        # Most importantly, we have to build words.
        # The character translations will have to be done word by word
        # as the formatting of a single character might depend on the
        # context.
        seg = None
        appendlist = []
        bases = {}
        sizes = {}
        for e in textline:
            if e.tag == "text":
                txt = (e.text or "")
                # txt = self._get_text_content(e)
                if txt == "":
                    print((u"Empty text in line:\n  {}".format(
                        xmlhelper.get_text(textline)).encode("UTF-8")))
                    xmlhelper.delete(e)
                elif txt.strip() == "":
                    # whitespace
                    if seg is not None:
                        appendlist.append(seg)
                    seg = self._create_seg("space")
                    seg.append(e)
                    e.text = " "
                    appendlist.append(seg)
                    seg = None
                elif txt.strip() == "/":
                    # slash is a word separator
                    if seg is not None:
                        appendlist.append(seg)
                    seg = self._create_seg("alphaNum")
                    seg.append(e)
                    appendlist.append(seg)
                    seg = None
                else:
                    if seg is None:
                        seg = self._create_seg("alphaNum")
                    seg.append(e)
                # size = float(e.get("size", "0.0"))
                size = float(e.get("msize", e.get("size", "0.0")))
                if size > 0.0:
                    try:
                        sizes[size] += 1
                    except KeyError:
                        sizes[size] = 1
                # base = self.get_base(e.get("bbox", None))
                base = self.get_base(e.get("origin", None))
                if base is not None:
                    try:
                        bases[base] += 1
                    except KeyError:
                        bases[base] = 1
            else:
                print(("Unexpected element {} in textline".format(e.tag)))
        # add final seg
        if seg is not None:
            appendlist.append(seg)
        for app_el in appendlist:
            textline.append(app_el)
        try:
            self.current_base = max([(bases[x], x) for x in bases])[1]
            # experimental: use a default font size if supplied
            if self.default_font_size is not None:
                self.current_size = self.default_font_size
            else:
                self.current_size = max([(sizes[x], x) for x in sizes])[1]
        except ValueError:
            print("Empty line?")
            print((textline.get("bbox", "nobbox")))
            parent = textline.getparent()
            while parent.tag != "page":
                parent = parent.getparent()
            pagenum = parent.get("id", "nopage")
            print(("on page {}".format(pagenum)))
        # Now that we have collected the words, we can set the
        # correct formatting word by word.
        self.wordcount = 0
        for seg in textline:
            if seg.get("type") == "space":
                seg.text = " "
                del seg[:]
            elif seg.get("type") == "alphaNum":
                self.wordcount += 1
                self.deal_with_word(seg)

    def get_base(self, bbox):
        """Determine base coordinate"""
        if bbox is None:
            return None
        values = [float(x) for x in bbox.split(",")]
        if len(values) == 4:
            return min([values[1], values[3]])
        elif len(values) == 2:
            return values[1]
        else:
            raise ConverterError("Cannot determine base of {}."
                    .format(bbox))

    def deal_with_word(self, seg):
        """Translate characters and set all formatting.
        
        Args:
            seg (Element): segment containing the word
        
        Supported formattings are:

        - italics
        - bold
        - fontname
        - fontsize
        - superscript
        - subscript
        - smallcaps

        Smallcaps have to be dealt with separately: if one or more
        characters in a word are smallcaps, we assume that the whole
        word is in smallcaps. Additionally we have to take into account
        the varying ways how lower case and upper case smallcpas are
        treated.
        """
        b_sc = False
        wd = ""
        xs = []
        ys = []
        wordsize, charsizes = self.get_wordsize(seg)
        for c in seg:
            b_generic_smallcaps = False
            # collect the bounding boxes to form the word bounding box
            bbox = c.get("bbox")
            if bbox:
                bbox = bbox.split(",")
                xs.append(float(bbox[0]))
                ys.append(float(bbox[1]))
                xs.append(float(bbox[2]))
                ys.append(float(bbox[3]))
            # character substitution
            replchar = c.text or ""
            fontname = c.get("font", "")
            style = self.guess_styles_from_fontname(fontname)
            # size = float(c.get("size", "0.0"))
            size = float(c.get("msize", c.get("size", "0.0")))
            rise = float(c.get("rise", "0.0"))
            style.size = size
            # base = self.get_base(c.get("bbox", None))
            base = self.get_base(c.get("origin", None))
            # special treatment of soft hyphen
            if self.replace_soft_hyphen and replchar == u"\u00ad":
                    replchar = u"-"
            else:
                if self.repltable is not None:
                    fonttable = self.repltable.get(fontname)
                    if fonttable is not None:
                        cid = int(c.get("cid", "-1"))
                        foundchar = (c.text or "").strip()
                        try:
                            replchar, replstyles = \
                                    fonttable["repl"][(foundchar, cid)]
                            # apply replstyles
                            for r in replstyles:
                                if r == "sc":
                                    style.smallcaps = True
                                    b_generic_smallcaps = True
                                elif r == "bold":
                                    style.bold = True
                                elif r == "italics":
                                    style.italics = True
                                else:
                                    print(("Unknown style: {}".format(r)))
                        except KeyError:
                            # no special style or replacement needed
                            pass
            # superscript, subscript
            if base > (self.current_base + 2.0) or rise > 2.0:
                style.valign = "super"
            elif base < (self.current_base - 2.0) or rise < -2.0:
                style.valign = "sub"
            else:
                # Base level letter; if it is upper case and also
                # smaller than the normal size, it is most probably
                # a lower case smallcaps character.
                # But note: also some type setting programs use a
                # slightly smaller font size for italics (probably for
                # optical reasons). Thus we have to set a certain
                # threshold. Usually with simulated smallcaps the size
                # is less than 80 % of the standard size (otherwise
                # the size difference would not be sufficiently noticable).
                if size < (self.current_size * 0.8) and replchar.isupper():
                    if not style.smallcaps:
                        style.smallcaps = True
            c.text = replchar
            wd += replchar
            # if (not style.smallcaps) and b_sc and replchar.isalpha():
            #     style.smallcaps = True
            if style.smallcaps:
                b_sc = True
            # adjust lower/upper in smallcaps word
            # @@@TODO:
            # But we may only transform characters if
            # the form does not yet contain the information
            # from the appropriate font encoding!
            # if c.get("font") == "KFRKEE+OriginalGaramondBT-Roman-SC750" and (c.get("bbox") == "87.874,309.602,92.673,317.911" or c.get("bbox") == "245.157,320.199,253.401,331.278"):
            #     import pdb; pdb.set_trace()
            if style.smallcaps and not b_generic_smallcaps:
                if size == wordsize and size < (self.current_size * 0.9):
                    c.text = c.text.lower()
                elif size >= self.current_size:
                    c.text = c.text.upper()
                else:
                    c.text = c.text.lower()
            elif style.smallcaps and b_generic_smallcaps:
                if size < (self.current_size * 0.8):
                    c.text = c.text.lower()
                elif size > (self.current_size * 1.2):
                    c.text = c.text.upper()
                elif c.get("font", "").find("SC750") != -1:
                    # @@@TODO: home made, pseudo-smallcaps font
                    c.text = c.text.upper()
                    # pass
                # elif size == self.current_size and wordsize < self.current_size:
                elif size == self.current_size and charsizes == self.MIXED:
                    # This seems to be a mixed word.
                    # @@@TODO:
                    # In some cases this leads to an erroneous transformation
                    # to upper case. Tests with the latest DA file (DA 73,2)
                    # indicate that this particular adjustment is not needed
                    # any more. But this needs more testing with older/other
                    # files.
                    # For the time being we emit a warning message, but refuse
                    # to change the character. Maybe a test is in order, if
                    # the current character value is from a replacement table.
                    # If this is the case, then no conversion should be
                    # performed.
                    logging.warning(
                        (u"Old algorithm suggests conversion to upper "
                         "case (%s): font: %s, size: %s, cid: %s"),
                        c.text,
                        fontname,
                        size,
                        c.get("cid", "-1")
                    )
                    # c.text = c.text.upper()
            if style.smallcaps:
                # c.set("size", str(self.current_size))
                c.set("msize", str(self.current_size))
                style.size = self.current_size
            ## if b_sc and (c.text or "").isalnum():
            ##     if size > wordsize and size < self.current_size:
            ##         c.text = c.text.upper()
            ##     elif size == self.current_size and not b_generic_smallcaps:
            ##         c.text = c.text.upper()
            ##     elif size < self.current_size:
            ##         c.text = c.text.lower()
            ##         c.set("size", str(self.current_size))
            ##         style.size = self.current_size
            styleid = self.add_style(style)
            c.set("rendition", "#" + styleid)
            # delete unneeded attributes
            xmlhelper.delat(c, "font")
            xmlhelper.delat(c, "bbox")
            xmlhelper.delat(c, "cid")
            xmlhelper.delat(c, "size")
            xmlhelper.delat(c, "msize")
            xmlhelper.delat(c, "origin")
            xmlhelper.delat(c, "rise")
            xmlhelper.delat(c, "glyphname")
            xmlhelper.delat(c, "color")
            xmlhelper.delat(c, "ncolor")
            xmlhelper.delat(c, "scolor")
            c.tag = "{{{}}}c".format(tei)
            # Could still be a smallcaps word, all letters are
            # upper case, but some are smaller than wordsize.
            # NB: It is also possible, that the whole word consists
            #     entirely of lower case smallcaps letters. We can
            #     only solve this, if we take a closer look at the
            #     font size in the whole textline (or better yet,
            #     the whole paragraph). But for the time being we
            #     assume that smallcaps are only ever used to mark
            #     surnames, which usually contain at least one upper
            #     case character (but cf. ``von Goethe``).
            # if wd == wd.upper() and len(sizes) > 1:
            #     # mixed sizes and all upper case characters
            #     b_sc = True
        bbox = [min(xs), min(ys), max(xs), max(ys)]
        bbox = ",".join([str(x) for x in bbox])
        wordid = "wd_{:05d}_{:03d}_{:03d}_{:02d}".format(
                self.pagecount, self.textboxcount,
                self.linecounter, self.wordcount)
        wordcoord = self.get_surface_coor({"bbox": bbox})
        wordcoord["{{{}}}id".format(xmlns)] = wordid
        seg.set("sameAs", "#" + wordid)
        zone = T.zone(wordcoord)
        zone.tail = "\n  "
        self.current_page_surface.append(zone)

    def get_word(self, seg):
        """Get text content"""
        ret = ""
        for c in seg:
            ret += (c.text or "")
        return ret

    def get_wordsize(self, seg):
        """Return mostly used font size within word"""
        sizes = {}
        for c in seg:
            # if (c.text or "").isalnum():
            if True:
                # size = float(c.get("size", "0.0"))
                size = float(c.get("msize", c.get("size", "0.0")))
                if size > 0.0:
                    sizes.update({size: sizes.get(size, 0) + 1})
        if len(sizes) == 0:
            # return 0.0
            return (0.0, self.CLEAN)
        sizelist = [(cnt, sz) for sz, cnt in list(sizes.items())]
        sizelist.sort(
                key=lambda x: (x[0], -x[1]),
                reverse=True)
        # sizelist.sort(
        #         cmp=lambda x,y: cmp((x[0],y[1]), (y[0],x[1])),
        #         reverse=True)
        # @@@TODO:
        # Make sure that the majority wins, but if there are two
        # or more sizes with equal number of occurrences, the
        # smallest size should win.
        return (sizelist[0][1], self.MIXED if len(sizes) > 1 else self.CLEAN)

    def guess_styles_from_fontname(self, fontname):
        """Try to make some assumptions about the style"""
        ret = styles.Style()
        # NB: This used to be a lot higher (0.1), but as a
        # result of better pdfminer size extraction, we use
        # a very small tolerance.
        ret.set_size_tolerance(0.01)
        if "SC" in fontname:
            # ret.append("sc")
            ret.smallcaps = True
        if "italic" in fontname.lower():
            # ret.append("italics")
            ret.italics = True
        if "bold" in fontname.lower():
            # ret.append("bold")
            ret.bold = True
        startpos = fontname.find("+")
        if startpos == -1:
            startpos = 0
        else:
            startpos += 1
        endpos = fontname.rfind("-")
        if endpos == -1:
            endpos = len(fontname)
        ret.fontname = fontname[startpos:endpos]
        return ret

    def deal_with_text(self, t):
        """Deal with single character"""
        t.tag = "{{{}}}c".format(tei)
        xmlhelper.delat(t, "font")
        xmlhelper.delat(t, "cid")
        xmlhelper.delat(t, "bbox")
        xmlhelper.delat(t, "size")
        xmlhelper.delat(t, "msize")

    def make_tei_header(self):
        """Create dummy header"""
        header = "<teiHeader xmlns=\"{}\">\n"\
                "<fileDesc>\n"\
                "<titleStmt>\n"\
                " <title></title>\n"\
                "</titleStmt>"\
                "\n<publicationStmt>\n"\
                "  <p></p>\n"\
                "</publicationStmt>\n"\
                "<sourceDesc>\n"\
                "  <p></p>\n"\
                "</sourceDesc>\n"\
                "</fileDesc>\n"\
                "<encodingDesc>\n"\
                "<styleDefDecl scheme=\"css\" schemeVersion=\"2.1\"/>\n"\
                "<editorialDecl>\n"\
                "<interpretation>\n"\
                " <ab>\n"\
                "  <interpGrp>\n"\
                "   <desc>Facsimile types</desc>\n"\
                "   <interp xml:id=\"facsScan\">list of scans</interp>\n"\
                "   <interp xml:id=\"facsCoor\">coordinates</interp>\n"\
                "  </interpGrp>\n"\
                "  <interpGrp>\n"\
                "   <desc>Scan labels</desc>\n"\
                "   <interp xml:id=\"mgh_ident\">MGH identifier for scan"\
                "</interp>\n"\
                "   <interp xml:id=\"sequenceNo\">scan number</interp>\n"\
                "   <interp xml:id=\"nativeNo\">page number</interp>\n"\
                "  </interpGrp>\n"\
                " </ab>\n"\
                "</interpretation>\n"\
                "</editorialDecl>\n"\
                "<tagsDecl>\n"\
                "</tagsDecl>\n"\
                "</encodingDesc>\n"\
                "</teiHeader>"\
                .format(tei)
        header_el = et.fromstring(header)
        header_el.tail = "\n"
        return header_el

    def write(self, outfile):
        """Write to outfile"""
        outfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".encode("UTF-8"))
        outfile.write(self.schematron_rules.encode("UTF-8"))
        outfile.write("\n".encode("UTF-8"))
        outfile.write(et.tostring(self.teidoc, encoding="UTF-8"))
        outfile.write("\n".encode("UTF-8"))

    def _get_xml_data(self, sourcefile):
        """Store XML representation fo file"""
        rm = PDFResourceManager(
                caching=True, font_correctors=self.font_correctors)
        laparams = LAParams()
        outfp = io.BytesIO()
        device = XMLConverter(rm, outfp, codec="UTF-8", laparams=laparams,
                imagewriter=None)
        interpreter = PDFPageInterpreter(rm, device)
        infile = open(sourcefile, "rb")
        pagenos = set()
        maxpages = 0
        rotation = 0
        password = ""
        for page in PDFPage.get_pages(
                infile,
                pagenos,
                maxpages=maxpages,
                password=password,
                caching=True,
                check_extractable=True):
            interpreter.process_page(page)
        infile.close()
        device.close()
        retval = outfp.getvalue()
        outfp.close()
        return retval

class MyFile(object):

    """
    This is only necessary because PDFMiner seems to mix unicode
    and byte strings happily.

    NB: This is probably resolved by now, so we can delete this class.
    """

    filebuffer = []
    #: classify this as a binary file
    mode = "b"

    def write(self, s):
        self.filebuffer.append(s)

    def getvalue(self):
        ret = []
        cnt_unicode = 0
        cnt_string = 0
        cnt_unknown = 0
        for s in self.filebuffer:
            if isinstance(s, unicode):
                ret.append(s.encode("UTF-8"))
                cnt_unicode += 1
                print((s.encode("UTF-8")))
            elif isinstance(s, str):
                ret.append(s)
                cnt_string += 1
            else:
                ret.append(str(s))
                logging.warning("Adding strange string object:\n"\
                        "\"" + str(s) + "\"")
                cnt_unknown += 1
        print(("{} unknown objects".format(cnt_unknown)))
        print(("{} string objects".format(cnt_string)))
        print(("{} unicode objects".format(cnt_unicode)))
        return "".join(ret)

    def close(self):
        self.filebuffer = []

