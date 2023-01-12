#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Help with font re-encoding.
"""

from io import open

from lxml import etree as et

def read(filename):
    """
    Read replacement table from filename.
    """
    ret = {}  # {fontname: {"repl": {
              #             (foundchar, cid):
              #                 (replchar, styles), ...
              #             }
              #         }
              #     }
    doc = et.HTML(open(filename, "br").read())
    for font in doc.xpath("//h1"):
        fontname = font.text
        ret[fontname] = {}
        ret[fontname]["repl"] = {}
        # skip over font metric information
        table = font.getnext()
        if table.tag == "p":
            table = table.getnext()
        assert(table.tag == "table")
        for tr in table.xpath("./tr"):
            foundchar = tr[0].text or ""
            if " " in foundchar and foundchar.strip() == "":
                foundchar = " "
            else:
                foundchar = foundchar.strip()
            replchar = tr[2].text or ""
            if " " in replchar and replchar.strip() == "":
                replchar = " "
            else:
                replchar = replchar.strip()
            cid = (tr[3].text or "").strip()
            if cid:
                cid = int(cid[cid.find(":")+1:].strip())
            else:
                cid = -1  # supposed to mean undefined
            cls = tr[2].get("class", "").strip()
            if cls != "":
                styles = [x.strip() for x in cls.split(" ")]
            else:
                styles = []
            if foundchar != replchar or len(styles) > 0:
                ret[fontname]["repl"][(foundchar, cid)] = (replchar, styles)
    return ret

