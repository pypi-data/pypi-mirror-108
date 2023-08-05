#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 14:45:20 2020

@author: bn
"""


from lxml import etree
from xml.sax.saxutils import escape, unescape
from io import StringIO, BytesIO
table_str = '''<questiontext format="html"><note><![CDATA[\n    <inline-para>\n      <para id="p1">\n        <p>=0</p>\n      </para>\n      <para id="p2">\n        <p>We recall that \n           \\(\\pi=\\)\n    3.141592653589793238.</p>\n      </para>\n      <para id="p3">\n        <p>What is the area of rectangle of height fp{trunc((1)+rand2*(10-1), 1)} and width fp{trunc(1+rand1*(10-1), 1)} ?</p>\n      </para>\n      <para id="p4">\n        <p>Check for random labels : fp{rand3 * rand4}</p>\n      </para>\n      <para id="p5">\n        <p>Check nested expression :\n\nfp{(1 + (pi+x)/(pi-x))}</p>\n      </para>\n      \n      \n    </inline-para>\n  ]]></note></questiontext>'''.replace('<br>','')
parser = etree.XMLParser(recover=True)  # needed because moodle may introduce html not well formed xml
root = etree.parse(StringIO(table_str), parser)
print(unescape(etree.tostring(root, encoding='utf8', pretty_print=True).decode()))
#root = etree.XML(table_str)
xslt_table = 'table.xslt'
transform = etree.XSLT(etree.parse(xslt_table))
tex = transform(root)
print(unescape(etree.tostring(tex, encoding='utf8', pretty_print=True).decode()))