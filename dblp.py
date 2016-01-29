#!/usr/bin/env python3

from lxml import etree

fs = {}

for _,e in etree.iterparse("dblp.xml", load_dtd=True):
    k = e.get('key')
    if k:
        if len(k.split('/')) < 3: continue
        ns,coll,_ = k.split('/', 2)
        if ns in ('www','homepages','tr','persons','phd'): continue
        fname = "%s/%s.bib" % (ns,coll)
        if fname not in fs:
            for other in fs: fs[other] = None
            fs[fname] = open(fname, 'w')
        f = fs[fname]
        print("@%s{%s," % (e.tag,k), file=f)
        author = []
        for child in e:
            t = child.tag
            v = etree.tostring(child, method='text', encoding='unicode').strip()
            v = v.replace('{','').replace('}','')
            if t == 'author':
                author.append(v)
                continue
            if t == 'title':
                if v[-1] == '.': v = v[:-1]
            if t == 'url': continue
            if t == 'ee':
                if v.startswith('http://dx.doi.org/'):
                    t = 'doi'
                    v = v[len('http://dx.doi.org/'):]
                else:
                    t = 'url'
            print("  %s = {%s}," % (t,v), file=f)
        print("  author = {%s}" % (' and '.join(author)), file=f)
        print("}", file=f)
        e.clear()
