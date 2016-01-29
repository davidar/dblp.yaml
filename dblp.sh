#!/bin/sh
wget http://dblp.uni-trier.de/xml/dblp.xml.gz
gunzip dblp.xml.gz
./dblp.py
for f in */*.bib; do
  echo $f
  pandoc-citeproc --bib2yaml $f > `dirname $f`/`basename $f .bib`.yaml
done
