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

magic = '__ESCAPED__P__'
citestart = re.compile(r'\\cite\{([^\\\}]+)\}')
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
    searchs = s.replace('\\%', magic).split('%')[0].replace(magic, '\\%')
    m = bibstart.match(s)

    if not m and not inbib:
        for citedata in citestart.findall(searchs):
            for cite in citedata.split(','):
                if not cite in order:
                    order.append(cite.strip())
        if bibend:
            afterbib += s
        else:
            beforebib += s
    elif not m and inbib:
        if '\\end{thebibliography}' in searchs:
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
        nbibname = (g[1] if g[1] else g[3]).strip()
        if inbib and bibname != nbibname: #move existing bib
            cites[bibname] = bib
            bib = ''
        bib += s
        bibname = nbibname
        inbib = True

propbib = ''

for cite in order:
    propbib += cites[cite]

print(propbib)

notcited = set(cites.keys()) - set(order)
