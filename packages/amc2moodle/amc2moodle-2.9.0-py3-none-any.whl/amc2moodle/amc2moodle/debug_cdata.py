#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:57:44 2021

@author: bn
"""


from lxml import etree

s = """<question><questiontext format="html"><note><![CDATA[
        <p>What is the <b>area</b> of rectangle of height {=((1)+{rand2}*(10-1))} and width {=(1+{rand1}*(10-1))} ?</p>
        <p>We recall that 
           \(\pi=\)
    3.141592653589793238 and 
           \(\pi&amp;lt;5\) </p>
        <p>Check for random labels : {=({rand3}*{rand4})}</p>
      
        <p>Check nested expression :
 {=((1+(pi()+(1))/(pi()-(1))))} =? 2.933884413848519720</p>
      
        <p>Check for power and trigo :
           \(\sin(0.5)^{2}+\cos(0.5)^{2}\)
     =  {=(pow(cos(0.5),1+1)+pow(sin(0.5),2))} =? 1</p>
      
  ]]></note></questiontext></question>"""


xslt = u"""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes" />
<!-- cdata-section-elements="xsltNote" -->
<!-- template identité -->
<xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
</xsl:template>

<xsl:template match="note"><xsltNote><xsl:apply-templates/></xsltNote></xsl:template>
</xsl:stylesheet>
"""
parser = etree.XMLParser(strip_cdata=False)
tree = etree.fromstring(s, parser)

transform = etree.XSLT(etree.fromstring(xslt.encode('utf8'), parser))
r = transform(tree)

for orig_text in tree.xpath(".//questiontext/note|.//note[@class='amc_bonne']/note|.//note[@class='amc_mauvaise']/note"):
    rawtext = (etree.tostring(orig_text, encoding='utf8')
                    .decode('utf-8')
                    .replace('<note>', '')
                    .replace('</note>', '')
                    .replace(r'\n', ''))
    # parse question
    # parsed_text = parser.render(rawtext)
    # questiontext.getparent().remove(questiontext)
    orig_text.clear()

    # FIXME this manipulation reveals a problem in the management of CDATA
    # fields created in transform2html. Since the orig_text.text contains only a part
    # of CDATA tag '<![CDATA[\n    '
    # this markup is ignored by xslt and transform.xslt process normally the elements
    # see orig_text.getchildren()[0]

    # orig_text.text = parsed_text  # works, CDATA already included
    # orig_text.text = etree.CDATA(parsed_text)  # doesn't work ??!!
    # Change behavior to avoid lxml unescape chars
    orig_text.text = etree.CDATA(etree.CDATA(rawtext.replace('<![CDATA[', '')
                                            .replace(']]>', '')
                                            .encode('utf8')))
    # this = etree.SubElement(tree, 'test')
    # this.text = etree.CDATA(rawtext.replace('<![CDATA[', '')
    #                                     .replace(']]>', '')
    #                                     .encode('utf8'))
out = etree.tostring(tree,  encoding="utf-8", pretty_print=True).decode('utf-8')

print(out)
print(etree.tostring(r,  encoding="utf-8", pretty_print=True).decode('utf-8'))
with open('toto.xml', 'w') as f:
    f.write(out)