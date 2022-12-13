#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Analyzer for PDF files
"""

import os.path
import logging

from lxml import etree as et
# from pdfimages import PDFImagesDocument
import fitz
from PIL import Image, ImageDraw
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

HTML_HEAD = u"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-type" content="text/html; charset=UTF-8"/>
<title>Fonts</title>
<style>
td {
  font-size:36pt;
  vertical-align:baseline;
}
td.bold {
  font-weight:bold;
}
td.sc {
  font-variant:small-caps;
}
td.italics {
  font-style:italic;
}
td.cid {
  font-size:12pt;
}
td.pic {
  font-size:18pt;
  padding-left:1em;
}
p.fontmetrics {
  margin-left: 40px;
  color: red;
}
</style>
</head>
<body>
"""

HTML_FOOT = u"""\
</body>
</html>
"""


class PDFAnalyzerError(Exception): pass

class Analyzer(object):
    """Analyzer for PDF files"""

    pdffile = ""
    xmlfile = ""
    imdir = ""
    fontdir = ""
    resolution = 0
    font_correctors = None  # list of FontCorrectors
    font_metrics = None  # some metrics for each font;
                         # this dict will only be populated if
                         # xml data is being extracted
    scales = (100.0, 100.0)

    b_make_images = True
    b_extract_xml_data = True
    b_extract_fonts = True

    def __init__(self, **kwargs):
        self.pdffile = kwargs.get("pdffile")
        if self.pdffile is None:
            raise PDFAnalyzerError("No PDF file specified.")
        if not os.path.isfile(self.pdffile):
            raise PDFAnalyzerError("{} is not a PDF file.".format(self.pdffile))
        self.xmlfile = kwargs.get("outfilename")
        if not self.xmlfile:
            self.xmlfile = os.path.splitext(self.pdffile)[0] + ".xml"
        self.imdir = kwargs.get("imdir", "imdir")
        self.fontdir = kwargs.get("fontdir", "fonts")
        if not os.path.isdir(self.imdir):
            os.makedirs(self.imdir)
        if not os.path.isdir(self.fontdir):
            os.makedirs(self.fontdir)
        self.resolution = kwargs.get("resolution", 300)
        self.b_make_images = kwargs.get("make_images", True)
        self.b_extract_xml_data = kwargs.get("extract_xml_data", True)
        self.b_extract_fonts = kwargs.get("extract_fonts", True)
        self.font_correctors = []
        font_correctors = kwargs.get("font_correctors")
        if font_correctors is not None:
            for fc in font_correctors:
                self.font_correctors.append(fc)
        self.scales = kwargs.get("scales", (100.0, 100.0))

    def analyze(self):
        """Start the program suite"""
        if self.b_make_images:
            self.images()
        if self.b_extract_xml_data:
            self.get_xml_data()
        if self.b_extract_fonts:
            self.extract_fonts()

    def images(self):
        """Create the images"""
        # pdf = PDFImagesDocument(self.pdffile)
        pdf = fitz.open(self.pdffile)
        # num_pages = pdf.count_pages()
        # num_pages = pdf.pageCount
        num_pages = pdf.page_count
        cnt = 1
        for idx in range(0, num_pages):
            imdata = pdf.get_page_pixmap(
                    idx,
                    matrix=fitz.Matrix(
                        float(self.resolution)/72,
                        float(self.resolution)/72
                    ),
                    colorspace="RGB",
                    alpha=False
                )
            im = Image.frombytes(
                    "RGB",
                    [imdata.w, imdata.h],
                    imdata.samples
                )
            basename = os.path.splitext(os.path.basename(self.pdffile))[0]
            name = "{}_{:05d}.jpg".format(basename, cnt)
            name = os.path.join(self.imdir, name)
            im.save(name, dpi=(self.resolution, self.resolution), quality=85)
            if not(cnt % 10):
                logging.info("  %d/%d", cnt + 1, num_pages)
            cnt += 1

    def extract_fonts(self):
        """Create HTML with all characters and images"""
        doc = et.parse(self.xmlfile)
        with open(os.path.join(self.fontdir, "index.htm"), "wb") as outfile:
            self.write_font_index(outfile, doc)

    def blow_up_bbox(self, bbox, scales=None):
        """
        Scale the bbox in vertical and horizontal direction,
        values in percent.
        """
        if scales is None:
            scales = self.scales
        horz = scales[0]/100.0
        vert = scales[1]/100.0
        bbox = [float(x) for x in bbox.split(",")]
        width_diff = (abs(bbox[0] - bbox[2])*horz - abs(bbox[0] - bbox[2]))/2
        height_diff = (abs(bbox[1] - bbox[3])*vert - abs(bbox[1] - bbox[3]))
        bbox[0] -= width_diff
        bbox[2] += width_diff
        if bbox[1] > bbox[3]:
            # bbox[1] += height_diff
            bbox[3] -= height_diff
        else:
            # bbox[1] -= height_diff
            bbox[3] += height_diff
        return ",".join([str(x) for x in bbox])

    def _is_smallcaps(self, glyphname):
        return glyphname.strip().lower().endswith(".sc")

    def write_font_index(self, outfile, doc):
        """Write font information into HMTL file"""
        outfile.write(HTML_HEAD.encode("UTF-8"))
        fonts = {}
        imgcount = 0
        for page in doc.xpath("//page"):
            current_page = page.get("id")
            for text in page.xpath(".//text"):
                font = text.get("font")
                if font is not None:
                    if fonts.get(font, None) is None:
                        fonts[font] = {}
                    txt = text.text or ""
                    cid = text.get("cid", "")
                    glyphname = text.get("glyphname", u"")
                    letterref = (txt, cid)
                    if not(txt == "\n" or txt == "\r" or txt == "\r\n" or \
                            txt == "\n\r"):
                        letter = fonts[font].get(letterref, None)
                        if letter is None:
                            textline = text.getparent()
                            lbox = self.blow_up_bbox(textline.get("bbox", ""), scales=self.scales)
                            fonts[font][letterref] = {
                                    "bbox": self.blow_up_bbox(text.get("bbox", None), scales=self.scales),
                                    "page": int(current_page),
                                    "img": imgcount,
                                    "sc": self._is_smallcaps(glyphname),
                                    "linebox": lbox}
                            imgcount += 1
        tags = set()
        for tl in doc.xpath("//textline"):
            for e in tl:
                tags.add(e.tag)
        fontnames = list(fonts.keys())
        fontnames.sort()
        pages = {}
        # build toc
        fontcount = 0
        outfile.write(("<p>\n").encode("UTF-8"))
        for font in fontnames:
            outfile.write("<a href=\"#f{}\">{}</a><br/>\n"
                    .format(fontcount, font).encode("UTF-8"))
            if self.font_metrics is not None:
                fm = self.font_metrics.get(font)
                if fm is not None:
                    outfile.write(
                            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                            "BBox: {}, Descent: {}<br/>\n"
                            .format(fm["bbox"], fm["descent"]).encode("UTF-8"))
            fontcount += 1
        outfile.write(("\n</p>\n").encode("UTF-8"))
        fontcount = 0
        for font in fontnames:
            basefontname = font
            pos = basefontname.find("+")
            if pos != -1:
                basefontname = basefontname[pos + 1:]
            outfile.write(("<h1 id=\"f" + str(fontcount) +
                "\">" + font + "</h1>\n").encode("UTF-8"))
            fontcount += 1
            # font metrics
            if self.font_metrics is not None:
                fm = self.font_metrics.get(font)
                if fm is not None:
                    outfile.write(u"<p class=\"fontmetrics\">\n".encode("UTF-8"))
                    outfile.write(
                            u"BBox: {}<br/>\n"
                            .format(fm["bbox"]).encode("UTF-8"))
                    outfile.write(
                            u"Descent: {}<br/>\n"
                            .format(fm["descent"]).encode("UTF-8"))
                    outfile.write("\n</p>\n".encode("UTF-8"))
            chars = list(fonts[font].keys())
            chars.sort()
            outfile.write(u"<table>\n".encode("UTF-8"))
            styles = []
            if "bold" in basefontname.lower():
                styles.append("bold")
            if "italic" in basefontname.lower():
                styles.append("italics")
            if "SC" in basefontname or "smallcaps" in basefontname.lower():
                styles.append("sc")
            style = " ".join(styles).strip()
            for char in chars:
                letterstyle = style
                if fonts[font][char]["sc"]:
                    if letterstyle:
                        letterstyle += " sc"
                    else:
                        letterstyle += "sc"
                bbox = [float(x) for x in fonts[font][char]["bbox"].split(",")]
                width = int((bbox[2] - bbox[0])/72*self.resolution)
                height = int((bbox[3] - bbox[1])/72*self.resolution)
                outfile.write(u"<tr>\n".encode("UTF-8"))
                outfile.write((u"<td class=\"" + letterstyle + "\">" + self._escape(char[0]) + "</td>\n").encode("UTF-8"))
                outfile.write((u"<td><img src=\"pic/outpic").encode("UTF-8"))
                outfile.write((u"%d.jpg\"" % fonts[font][char]["img"])\
                        .encode("UTF-8"))
                outfile.write((u" width=\"%d\" " % width).encode("UTF-8"))
                outfile.write((u"height=\"%d\"/></td>\n" % height)\
                        .encode("UTF-8"))
                outfile.write((u"<td class=\"" + letterstyle + "\">" + self._escape(char[0]) + "</td>\n").encode("UTF-8"))
                outfile.write((u"<td class=\"cid\">CID: " \
                        + char[1] + "</td>\n").encode("UTF-8"))
                # line context
                linebox = [float(x)
                        for x in fonts[font][char]["linebox"].split(",")]
                linewidth = int((linebox[2] - linebox[0])/72*self.resolution)/3
                lineheight = int((linebox[3] - linebox[1])/72*self.resolution)/3
                outfile.write((u"<td><img src=\"pic/linepic").encode("UTF-8"))
                outfile.write((u"%d.jpg\"" % fonts[font][char]["img"])\
                        .encode("UTF-8"))
                outfile.write((u" width=\"%d\" " % linewidth).encode("UTF-8"))
                outfile.write((u"height=\"%d\"/></td>\n" % lineheight)\
                        .encode("UTF-8"))
                outfile.write((u"<td>Scan: %d</td>\n" %\
                        fonts[font][char]["page"]).encode("UTF-8"))
                # end line context
                outfile.write((u"<td class=\"pic\">Pic: %d</td>\n" %\
                        fonts[font][char]["img"]).encode("UTF-8"))
                outfile.write(u"</tr>\n".encode("UTF-8"))
                # add image to pages
                pagenum = fonts[font][char]["page"]
                pg = pages.get(pagenum, None)
                if pg is None:
                    pg = []
                    pages[pagenum] = pg
                pg.append((fonts[font][char]["img"], fonts[font][char]["bbox"],
                    fonts[font][char]["linebox"]))
            outfile.write((u"</table>\n").encode("UTF-8"))
        # create images
        outdir = os.path.join(self.fontdir, "pic")
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        for p in list(pages.keys()):
            basename = os.path.splitext(os.path.basename(self.pdffile))[0]
            source_imgname = os.path.join(
                self.imdir, "{}_{:05d}.jpg".format(basename, p)
            )
            img = Image.open(source_imgname)
            for imnum, bbox, linebox in pages[p]:
                imgfilename = os.path.join(outdir, "outpic%d.jpg" % imnum)
                box = [float(x) for x in bbox.split(",")]
                box = [x/float(72)*self.resolution for x in box]
                tmp = img.size[1] - box[1]
                box[1] = img.size[1] - box[3]
                box[3] = tmp
                box = [int(x) for x in box]
                # Problem with some combining diacritical characters
                # in Junicode font: they seem to have to vertical
                # extension, thus x1 and x2 are the same. This leads
                # to problems with the cropbox. Thus: if x- or y-values
                # are the same, we extend the cropbox.
                oldbox = None
                if box[0] == box[2]:
                    oldbox = [x for x in box]
                    box[0] -= 5
                    box[2] += 5
                    if box[0] < 0:
                        box[0] = 0
                if box[1] == box[3]:
                    if not oldbox:
                        oldbox = [x for x in box]
                    box[1] -= 5
                    box[3] += 5
                    if box[1] < 0:
                        box[1] = 0
                if oldbox:
                    logging.info("Corrected cropbox %s --> %s",
                        oldbox,
                        box
                    )
                try:
                    img2 = img.crop(box)
                except (MemoryError,) as memerr:
                    logging.error(
                        ("%s: imagefilename: %s, box: %s, img: %s, "
                         "bbox: %s, size: (%d, %d)"),
                         memerr,
                         imgfilename,
                         box,
                         source_imgname,
                         bbox,
                         img.size[0],
                         img.size[1]
                    )
                    raise
                try:
                    img2.save(imgfilename)
                except (SystemError,) as syserr:
                    logging.error(
                        ("%s: imagefilename: %s, box: %s, img: %s,"
                         "bbox: %s, size: (%d, %d)"),
                        syserr,
                        imgfilename,
                        box,
                        source_imgname,
                        bbox,
                        img.size[0],
                        img.size[1]
                    )
                    raise
                del img2
                imgfilename = os.path.join(outdir, "linepic%d.jpg" % imnum)
                box2 = [float(x) for x in linebox.split(",")]
                box2 = [x/float(72)*self.resolution for x in box2]
                tmp = img.size[1] - box2[1]
                box2[1] = img.size[1] - box2[3]
                box2[3] = tmp
                box2 = [int(x) for x in box2]
                img2 = img.crop(box2)
                draw = ImageDraw.Draw(img2)
                draw.line([box[0]-box2[0], box[3]-box2[1],
                    box[2]-box2[0], box[3]-box2[1]], fill=0x0000ff, width=14)
                img2.save(imgfilename)
                del img2
        # tags = list(tags)
        # tags.sort()
        # print("")
        # print("Tags (under textline):")
        # for t in tags:
        #     print("  " + t)
        outfile.write(HTML_FOOT.encode("UTF-8"))
        outfile.close()

    def _escape(self, s):
        s = s.replace(u"&", u"&amp;")
        s = s.replace(u"<", u"&lt;")
        s = s.replace(u">", u"&gt;")
        return s

    def get_xml_data(self):
        """Store XML representation of file"""
        rm = PDFResourceManager(
                caching=True, font_correctors=self.font_correctors)
        laparams = LAParams()
        outfp = open(self.xmlfile, "wb")
        device = XMLConverter(rm, outfp, codec="UTF-8", laparams=laparams,
                imagewriter=None)
        interpreter = PDFPageInterpreter(rm, device)
        infile = open(self.pdffile, "rb")
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
            page.rotate = (page.rotate + rotation) % 360
            interpreter.process_page(page)
        self.font_metrics = {}
        for font in list(rm._cached_fonts.values()):
            try:
                self.font_metrics[font.fontname] = {"bbox": font.bbox,
                        "descent": font.descent}
            except AttributeError:
                print((dir(font)))
        infile.close()
        device.close()
        outfp.close()

