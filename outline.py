#! /usr/bin/env python3
import pikepdf
mydoc = pikepdf.open("outline.pdf")
#print(repr(mydoc.Root['/Outlines']))
#print(repr(mydoc.Root['/Names']['/Dests']['/Kids']))
#print(repr(mydoc.Root))
#print(repr(mydoc))
for k in mydoc.Root['/Names']['/Dests']['/Kids']:
    print('**********************')
    for i in range(len(k.Names)):
        if i%2 == 0:
            print(k.Names[i])
with mydoc.open_outline() as outline:
    for o in outline:
        print(dir(o))
    for o in outline.root:
    # §12.6.4.2 in PDF specification
        print(o.action.D, o.title)
        for oo in o:
            print(repr(oo))
    # §12.3 in PDF specification
    # §12.3.3 in PDF specification
    # §12.3.2.2 Named Destinations
    # §12.3.2.3 Named Destinations
    #print(o.destination)
    #print(o.title)
