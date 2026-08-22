# -*- coding: utf-8 -*-
"""Görselli sayfa başlığı (.dh-ph--photo) — iletisim.html'deki kalıp.

Üreteçlerin hepsi bunu kullanır ki yeni sayfalar sitenin başlık
standardından sapmasın. Kırıntı --ink varyantına geçer (görsel üstünde
okunsun diye), sayfa adı h1'dir ve sayfada tek h1 odur.
"""

def basli(kicker, baslik, lead, crumb, gorsel, poz="50% 50%", meta=None):
    """crumb: [(metin, href|None), ...] — son öğe aria-current alır."""
    o = []
    w = o.append
    w('    <header class="dh-ph dh-ph--photo">\n')
    w('      <span class="dh-vmedia" style="--dh-vpos: %s" aria-hidden="true">\n' % poz)
    w('        <img src="./assets/images/main/posts/%s" alt="" loading="eager" fetchpriority="high" decoding="async">\n' % gorsel)
    w('      </span>\n')
    w('      <div class="container max-w-xl">\n')
    w('        <nav class="dh-art-crumb dh-art-crumb--ink" aria-label="Sayfa yolu">\n')
    w('          <a href="index.html" aria-label="Anasayfa"><i class="fas fa-home-lg-alt" aria-hidden="true"></i></a>\n')
    for i, (ad, href) in enumerate(crumb):
        w('          <i class="fas fa-chevron-right" aria-hidden="true"></i>\n')
        if href and i < len(crumb) - 1:
            w('          <a href="%s">%s</a>\n' % (href, ad))
        else:
            w('          <span aria-current="page">%s</span>\n' % ad)
    w('        </nav>\n\n')
    w('        <span class="dh-ph__bar" aria-hidden="true"></span>\n')
    w('        <span class="dh-ph__eyebrow">%s</span>\n' % kicker)
    w('        <h1 class="dh-ph__title">%s</h1>\n' % baslik)
    w('        <p class="dh-ph__sub">%s</p>\n' % lead)
    if meta:
        w('        <div class="dh-ph__meta">\n')
        for i, m in enumerate(meta):
            if i:
                w('          <span class="dh-ph__sep" aria-hidden="true"></span>\n')
            w('          <span>%s</span>\n' % m)
        w('        </div>\n')
    w('      </div>\n    </header>\n\n')
    return "".join(o)
