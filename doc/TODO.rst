****
TODO
****

- Transformation der von anapdf erzeugten [Band].xml anpassen (aoe, 2022-04-13):

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

======================================================================

- Bugfix anapdf (aoe, 2022-04-13):

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


======================================================================

- emit logging messages while hacking apart files

