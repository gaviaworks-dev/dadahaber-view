# -*- coding: utf-8 -*-
"""81 il verisi — TEK KAYNAK.

iller-uret.py ve hava-uret.py aynı listeyi kullanıyor. İkisine ayrı ayrı
yazılsaydı biri güncellenip diğeri unutulurdu; buraya alındı.
"""

ILLER = """Adana Adıyaman Afyonkarahisar Ağrı Amasya Ankara Antalya Artvin Aydın Balıkesir
Bilecik Bingöl Bitlis Bolu Burdur Bursa Çanakkale Çankırı Çorum Denizli
Diyarbakır Edirne Elazığ Erzincan Erzurum Eskişehir Gaziantep Giresun Gümüşhane Hakkâri
Hatay Isparta Mersin İstanbul İzmir Kars Kastamonu Kayseri Kırklareli Kırşehir
Kocaeli Konya Kütahya Malatya Manisa Kahramanmaraş Mardin Muğla Muş Nevşehir
Niğde Ordu Rize Sakarya Samsun Siirt Sinop Sivas Tekirdağ Tokat
Trabzon Tunceli Şanlıurfa Uşak Van Yozgat Zonguldak Aksaray Bayburt Karaman
Kırıkkale Batman Şırnak Bartın Ardahan Iğdır Yalova Karabük Kilis Osmaniye
Düzce""".split()

BOLGE = {
 "Marmara": "İstanbul Bursa Kocaeli Tekirdağ Balıkesir Çanakkale Edirne Kırklareli Sakarya Bilecik Yalova".split(),
 "Ege": "İzmir Manisa Aydın Denizli Muğla Afyonkarahisar Kütahya Uşak".split(),
 "Akdeniz": "Antalya Adana Mersin Hatay Isparta Burdur Kahramanmaraş Osmaniye".split(),
 "İç Anadolu": "Ankara Konya Kayseri Eskişehir Sivas Yozgat Aksaray Karaman Kırıkkale Kırşehir Nevşehir Niğde Çankırı".split(),
 "Karadeniz": ("Samsun Trabzon Ordu Rize Giresun Zonguldak Bolu Düzce Karabük Bartın Kastamonu "
               "Sinop Çorum Amasya Tokat Artvin Gümüşhane Bayburt").split(),
 "Doğu Anadolu": "Erzurum Van Malatya Elazığ Ağrı Kars Erzincan Bingöl Bitlis Hakkâri Muş Tunceli Ardahan Iğdır".split(),
 "Güneydoğu Anadolu": "Gaziantep Şanlıurfa Diyarbakır Mardin Batman Adıyaman Siirt Şırnak Kilis".split(),
}
IL_BOLGE = {il: b for b, ler in BOLGE.items() for il in ler}


def kisalt(il):
    """Izgara kutusu 62px; sekiz karakterden uzun ad taşıyor.
    Tam ad her kutunun <title>'ında duruyor."""
    return il if len(il) <= 8 else il[:7] + "."


def anahtar(il):
    d = str.maketrans("çğıöşüÇĞİÖŞÜâ ", "cgiosucgiosua-")
    return il.translate(d).lower()
