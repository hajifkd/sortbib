#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sortbib.py
# created by H.Fukuda

import sys
import re

if len(sys.argv) != 2:
    print("usage: python sortbib.py")
    sys.exit(1)

f = open(sys.argv[1])

bibstart = re.compile(r'^\s*(%\\cite\{(.+)\})|(\\bibitem\{(.+)\})\s*$')
inbib = False
bibend = False
bib = ''
bibname = ''
order = []
cites = {}
beforebib = ''
afterbib = ''

for s in f.readlines():
    m = bibstart.match(s)
    if not m and not inbib:
        if bibend:
            afterbib += s
        else:
            beforebib += s
    elif not m and inbib:
        if '\\end{thebibliography}' in s:
            cites[bibname] = bib
            bib = ''
            bibname = ''
            bibend = True
            inbib = False
            afterbib = s
        else:
            bib += s
    elif m: #bib starts
        g = m.groups()
        nbibname = g[1] if g[1] else g[3]
        if inbib and bibname != nbibname: #move existing bib
            cites[bibname] = bib
            bib = ''
        bib += s
        bibname = nbibname
        inbib = True


print('begin cites')
print(cites)

print('after cites')
print(afterbib)
