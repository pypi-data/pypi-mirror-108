#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 14:28:37 2020

@author: bn
"""

import markdown
s = "<text><![CDATA[\ntext formatting\nGo to your editor preferences (via the user menu) and select 'Plain text area', then in the question box, select **Markdown format**.\nGo to your editor preferences (via the user menu) and select 'Plain text area', then in the question box, select **Markdown format**.\n\n]]></text>\n    "

cdata_content = markdown.markdown(s, extensions=['extra'])