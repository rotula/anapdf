****
TODO
****

- How is the CID used in font handling (correction, encoding)?
- What does the ``fc_base.py`` do? Is it OK, if one input Unicode code point appears
  twice within a font in ``index.htm`` but with a different CID? (lower/upper case
  characters in some fonts) How to do this in ``fc_base.py``?
- How does PDF, how does PDFMiner etc. deal with soft hyphens?

Transformation der von anapdf erzeugten [Band].xml anpassen (aoe, 2022-04-13):
==============================================================================

Im Bereich der römischen Seitenzahlen wird momentan in <page> der Wert von @label nur im Fall der ersten Seite ("I") korrekt eingetragen.
Alle weiteren scheinen von der ersten arabischen Seitenzahl (ggf. über Null) heruntergezählt zu werden. 

Zwei Beispiele: 

(1) MGH Epp. 8,2 (BSB 2034) setzt im Editionsteil die Paginierung von Epp. 8,1 mit S. 229 fort, die Seiten der Einleitung (pp. II-VIII) sind in mgh_epp_8_2.xml als "222"-"228" gelabelt:

<page id="1" bbox="0.000,0.000,538.583,751.181" rotate="0" label="I">
...
<page id="2" bbox="0.000,0.000,538.583,751.181" rotate="0" label="222">
...
<page id="8" bbox="0.000,0.000,538.583,751.181" rotate="0" label="228">
...
<page id="9" bbox="0.000,0.000,595.276,822.047" rotate="0" label="229">


(2) MGH SS rer. Germ. 82 (BSB 2013) hat demgenüber eine "genuine", im Editionsteil mit "1" einsetzende arabische Paginierung. 
Hier erhalten die im Band römisch gezählten Einleitungsseiten in mgh_ss_rer_germ_82.xml eine Minus-Zahl bzw. "0" als Wert von @label:

<page id="1" bbox="0.000,0.000,419.528,643.465" rotate="0" label="I">
...
<page id="2" bbox="0.000,0.000,419.528,643.465" rotate="0" label="-14">
...
<page id="16" bbox="0.000,0.000,419.528,643.465" rotate="0" label="0">
...
<page id="17" bbox="0.000,0.000,419.528,643.465" rotate="0" label="1">


Bugfix anapdf:
==============
Im Fall von BSB 2256 = MGH Hebr. Texte 2,2 bricht anapdf mit folgender Fehlermeldung ab:
fonts/index.htm: anapf scheint hier auf ein Problem gestoßen zu sein: einige Zeichen werden nicht als Snippet angezeigt, weswegen eine Prüfung nicht möglich ist. Fehlermeldung:

Traceback (most recent call last):
  File "C:\ProgramData\Anaconda3\Scripts\anapdf-script.py", line 33, in <module>
    sys.exit(load_entry_point('anapdf', 'console_scripts', 'anapdf')())
  File "c:\users\andreas öffner\git\anapdf\src\anapdf\scripts\anapdf_script.py", line 108, in main
    a.analyze()
  File "c:\users\andreas öffner\git\anapdf\src\anapdf\analyzer.py", line 106, in analyze
    self.extract_fonts()
  File "c:\users\andreas öffner\git\anapdf\src\anapdf\analyzer.py", line 142, in extract_fonts
    self.write_font_index(outfile, doc)
  File "c:\users\andreas öffner\git\anapdf\src\anapdf\analyzer.py", line 381, in write_font_index
    img2.save(imgfilename)
  File "C:\ProgramData\Anaconda3\lib\site-packages\PIL\Image.py", line 2240, in save
    save_handler(self, fp, filename)
  File "C:\ProgramData\Anaconda3\lib\site-packages\PIL\JpegImagePlugin.py", line 782, in _save
    ImageFile._save(im, fp, [("jpeg", (0, 0) + im.size, 0, rawmode)], bufsize)
  File "C:\ProgramData\Anaconda3\lib\site-packages\PIL\ImageFile.py", line 531, in _save
    e.setimage(im.im, b)
SystemError: tile cannot extend outside image


Optimierung anapdf:
==================
Im Fall von (z.B.?) BSB 2044 und 2053 extrahiert anapdf offenbar Text, der in der PDF als Ergebnis der InDesign-Bearbeitung als Überrest oder Dublette vorhanden, aber nicht sichtbar ist (transparente Farbe?). 
Beispiele:

- BSB 2044, S. (II) = img 00002: Überrest: "Konstanzer Domkapitels", "Teil 1" 
- BSB 2044, S. (III) = img 00003: Überrest: "Konstanzer Domkapitels", "Teil 1"), 
- BSB 2044, S. 5 = img 000037: Dublette: "Graphisches Lagenschema vor der Restaurierung"; Überrest/Dublette mit S. 6: "Graphisches Lagenschema nach der Restaurierung (2008) gemäß der (korrigierten) Rekonstruktion von Schmid"
- BSB 2044, S. 6 = img 000038: Dublette: "Älteres Gedenkbuch"; Dublette: "Lose Blätter"; Dublette: "Nonantola-Doppelblatt"
- BSB 2053, S. XII = img 000012: Dublette: "Inhaltsverzeichnis"/"Inhaltsverzeichnis"



Bugfix pdf2tei (cra/aoe, 2022-04-14)
=====================================

Transformation von BSB 2257 funktioniert (BSB-tei.xml wird augsgegeben), aber mit folgender Fehlermeldung:

C:\Users\Andreas Öffner\MGH Dropbox\Andreas Öffner\Projekte\dmgh\2257\extract>pdf2tei -f fonts\index.htm ..\mgh_ss_rer_germ_83.xml
Empty line?
56.070,462.146,70.806,465.482
on page 357
Empty line?
... 

>> Hat das mit dem Wechsel von seitenbreitem Text und Spalten auf ein und derselben Seite zu tun?



Bugfix pdfminer (aoe, 2022-04-13)
==================================

Im Fall von BSB 2044 (MGH Libri mem. N. S. 8) gibt es ein Problem mit dem pdf mining: 

INFO:pdfminer.pdfpage:Page: {'ArtBox': [0.0, 0.0, 637.795, 890.079], 'BleedBox': [0.0, 0.0, 637.795, 890.079], 'Contents': <PDFObjRef:72>, 'CropBox': [0.0, 0.0, 637.795, 890.079], 'MediaBox': [0.0, 0.0, 637.795, 890.079], 'Parent': <PDFObjRef:197996>, 'Resources': {}, 'Rotate': 0, 'TrimBox': [0.0, 0.0, 637.795, 890.079], 'Type': /'Page'}
Traceback (most recent call last):
  File "C:\ProgramData\Anaconda3\Scripts\anapdf-script.py", line 33, in <module>
    sys.exit(load_entry_point('anapdf', 'console_scripts', 'anapdf')())
  File "c:\users\andreas öffner\git\anapdf\src\anapdf\scripts\anapdf_script.py", line 108, in main
    a.analyze()
  File "c:\users\andreas öffner\git\anapdf\src\anapdf\analyzer.py", line 105, in analyze
    self.get_xml_data()
  File "c:\users\andreas öffner\git\anapdf\src\anapdf\analyzer.py", line 412, in get_xml_data
    for page in PDFPage.get_pages(
  File "C:\ProgramData\Anaconda3\lib\site-packages\pdfminer\pdfpage.py", line 191, in get_pages
    for (pageno, page) in enumerate(klass.create_pages(doc)):
  File "C:\ProgramData\Anaconda3\lib\site-packages\pdfminer\pdfpage.py", line 161, in create_pages
    label = get_label(fullnumtree, cnt)
  File "C:\ProgramData\Anaconda3\lib\site-packages\pdfminer\pdfpage.py", line 122, in get_label
    return prefix + value
TypeError: can't concat str to bytes

>> Nach dem Update von pdfminer (2017/2020) scheint dieser Teil nun zu funktionieren, aber die xml-Erstellung terminiert erst nach sehr langer Zeit.



emit logging messages while hacking apart files (cra)
======================================================

