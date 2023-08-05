#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:24:10 2020

@author: bn
"""

from lxml import etree
from xml.sax.saxutils import escape, unescape
from io import StringIO, BytesIO
table_str = '''
<?xml version="1.0" encoding="UTF-8"?>
<document>
  <para xml:id="p1">
    <p>
      <text class="amc_baremeDefautS">e=-0.5,b=1,m=-0.5</text>
      <text class="amc_baremeDefautM">e=-0.5,b=1,m=-0.25,p=-0.5</text>
    </p>
  </para>
  <note class="amc_categorie">cat1</note>
  <note class="amc_questionmult" role="Qmult:Aucune">
    <inline-para>
      <para xml:id="p2">
        <p><text class="amc_bareme">e=-0.5,b=1,m=-1.,p=-0.5</text> Quel fruit possède un noyau?
<note class="amc_choices_options">o</note>
<note class="amc_mauvaise">La pomme</note>
<note class="amc_mauvaise">La tomate</note>
<note class="amc_mauvaise">le Kiwi</note></p>
      </para>
    </inline-para>
  </note>
  <note class="amc_categorie">cat1</note>
  <note class="amc_questionmult" role="bcl1a">
    <inline-para>
      <para xml:id="p3">
        <p>Combien de fois le programme suivant affiche-t-il <text font="typewriter">"x"</text> ?</p>
      </para>
      <para xml:id="p4">
        <p><text font="typewriter">for (int i = 4; i &lt; 24; ++i)<break/> for (int j = i + 2; j - 1 &gt; 0; --j)<break/>  puts("x");</text></p>
      </para>
      <note class="amc_numeric_choices" role="digits=3,sign=false,scoreexact=2,scoreapprox=1,approx=10">290</note>
    </inline-para>
  </note>
</document>
'''.replace('<br>','')
parser = etree.XMLParser(recover=True)  # needed because moodle may introduce html not well formed xml
root = etree.parse(StringIO(table_str), parser)
print(unescape(etree.tostring(root, encoding='utf8', pretty_print=True).decode()))
#root = etree.XML(table_str)
xslt_table = 'transform_qtype.xslt'
transform = etree.XSLT(etree.parse(xslt_table))
tex = transform(root)
print(etree.tostring(tex, encoding='utf8', pretty_print=True).decode())