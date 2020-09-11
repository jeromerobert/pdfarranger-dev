#! /usr/bin/env python3
import pikepdf
mydoc = pikepdf.open("dessin_d.pdf")
src_page = mydoc.pages[0]
label = b'/p0'
new_page = pikepdf.Dictionary(
   Type = pikepdf.Name.Page,
   MediaBox = [0, 0, 595.275574*2, 841.889771*2],
   Contents = mydoc.make_stream(b"q 2 0 0 2 0 0 cm " + label + b" Do Q"),
   Resources = {'/XObject' : {label: pikepdf.Page(src_page).as_form_xobject() }},
)
mydoc.pages.insert(0, new_page)
del mydoc.pages[1]
mydoc.save("toto.pdf", compress_streams=False)
