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
<doc>
    <p><img></p>
    <table>
        <caption style="caption-side: bottom">basic table</caption>
        <thead>
        	<tr>
        		<th scope="col">h1</th>
        		<th scope="col">h2</th>
        		<th scope="col">h3</th>
        	</tr>
        </thead>
        <tbody>
        	<tr>
        		<td>d1</td>
        		<td>d2</td>
        		<td>d3</td>
        	</tr>
        </tbody>
    </table>
    <table>
        <caption style="caption-side: bottom">table legend</caption>
        <thead>
            <tr>
                <th scope="col">12</th>
                <th scope="col">weight</th>
                <th scope="col">width</th>
                <th scope="col">length</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <th scope="row">sys1</th>
                <td>1 kg<br></td>
                <td>0.35 m<br></td>
                <td> 1 m<br></td>
            </tr>
            <tr>
                <th scope="row">sys2</th>
              <td>2 kg<br></td>
              <td>-</td>
              <td>1.5 m<br></td>
            </tr>
        </tbody>
    </table>
    <table>
<caption style="caption-side: bottom"></caption>
<thead>
<tr>
<th scope="col">stuff1<br></th>
<th scope="col">stuff2</th>
</tr>
</thead>
<tbody>
<tr>
<td>\(x^2\)<br></td>
<td>bold <b>text</b><br></td>
</tr>
</tbody>
</table>
</doc>
'''.replace('<br>','')
parser = etree.XMLParser(recover=True)  # needed because moodle may introduce html not well formed xml
root = etree.parse(StringIO(table_str), parser)
print(unescape(etree.tostring(root, encoding='utf8', pretty_print=True).decode()))
#root = etree.XML(table_str)
xslt_table = 'table.xslt'
transform = etree.XSLT(etree.parse(xslt_table))
tex = transform(root)
print(unescape(etree.tostring(tex, encoding='utf8', pretty_print=True).decode()))