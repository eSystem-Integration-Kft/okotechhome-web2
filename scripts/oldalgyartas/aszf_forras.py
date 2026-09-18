# -*- coding: utf-8 -*-
"""aszf_forras.py — a két ÁSZF-dokumentum beolvasása .docx-ből.

MIÉRT KÜLÖN MODUL. Az ÁSZF jogi szöveg: nem írjuk át, nem tömörítjük, nem
fogalmazzuk újra. A dolgunk annyi, hogy a Word-dokumentum bekezdéseit HIÁNYTALANUL
átvigyük a lapra, olvasható tagolással. Ezért a beolvasás és a megjelenítés külön
áll: ha a jogász új változatot küld, csak a fájlt kell cserélni.

AMIT A .DOCX-BŐL KIOLVASUNK
  · `<w:p>`      — bekezdés
  · `<w:br/>`    — soremelés a bekezdésen belül (az Eladó adatai így állnak)
  · `<w:tab/>`   — tabulátor
  · `<w:numPr>`  — listaelem (számozott vagy felsorolás)

A TAGOLÁS SZABÁLYA. A dokumentum nem használ Word-címstílusokat, a fejezetcímek
CSUPA NAGYBETŰS, rövid bekezdések. Ezt ismerjük fel; a kettősponttal végződő
rövid sor alcím. Minden más bekezdés marad bekezdésnek.
"""
import pathlib
import re
import unicodedata
import zipfile

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'



# ===========================================================================
# GÉPI CSEREHIBÁK JAVÍTÁSA
# ---------------------------------------------------------------------------
# A dokumentumon végigfutott egy „Ügyfél" → „Megrendelő" csere, ami olyan
# szavakat is átírt, amelyeknek nem volt szabad: `Ügyfélszolgálat` →
# `Megrendelőszolgálat`, `ügyfélfogadási idő` → `Megrendelőfogadási idő`. A
# névelő is bennragadt: `az Megrendelő` harmincötször. Ezek MECHANIKUS hibák,
# jogi tartalmuk nincs — a lapon a helyes alak áll. A `.docx` ÉRINTETLEN marad:
# a hiteles változat az, és a javított szöveget Bela viszi vissza a jogászhoz.
#
# A SORREND SZÁMÍT. Előbb a szóösszetételek (`Megrendelőszolgálat`), utána a
# névelő — különben az `az Ügyfélszolgálat` helyes alakot is elrontanánk.
# A webhely megnevezése a két dokumentumban eltérő zárójelezéssel áll (az
# egyikből hiányzik egy záró zárójel), ezért mintával cseréljük.
WEBOLDAL = re.compile(r'\(Biológiai szennyvíztisztítók 1-től 50 főig[^)]*\(okotechhome\.hu\)\)?')

JAVITAS = [
    ('https://okotechhome.hu/formok/megrendel.php', 'https://okotechhome.hu/megrendeles'),
    # az elrontott csere visszavezetése
    ('Megrendelőszolgálat', 'Ügyfélszolgálat'),
    ('Megrendelő szolgálati', 'ügyfélszolgálati'),
    ('Megrendelőfogadási', 'ügyfélfogadási'),
    ('az Megrendelő', 'a Megrendelő'),
    ('Az Megrendelő', 'A Megrendelő'),
    # írásmód és elgépelés
    ('Ökotech-Home', 'ÖkoTech-Home'),
    ('fogasztóvédelem', 'fogyasztóvédelem'),
]


def javit(s):
    # A Word helyenként pont nélküli i-t (U+0131) hagyott a vessző alatt:
    # `kijavı́thatja`, `teljesıt́ésével`. Az összevonás után lesz belőle `í`.
    s = unicodedata.normalize('NFC', s.replace('\u0131', 'i'))
    s = WEBOLDAL.sub('(Biológiai szennyvíztisztító rendszer — ÖkoTech-Home Kft., okotechhome.hu)', s)
    for regi, uj in JAVITAS:
        s = s.replace(regi, uj)
    return s


def _bekezdesek(ut):
    """(szöveg, listaelem-e) párok a dokumentum sorrendjében."""
    xml = zipfile.ZipFile(ut).read('word/document.xml').decode('utf-8')
    torzs = xml[xml.index('<w:body>'):]
    ki = []
    for p in re.findall(r'<w:p[ >].*?</w:p>|<w:p/>', torzs, re.S):
        lista = '<w:numPr>' in p
        # A soremelés és a tabulátor VALÓDI tagolás a szerződésben (az Eladó
        # adatai egyetlen bekezdésben, sortörésekkel állnak) — megtartjuk.
        t = re.sub(r'<w:br\s*/>', '\n', p)
        t = re.sub(r'<w:tab\s*/>', '\t', t)
        t = re.sub(r'<[^>]+>', '', t)
        t = t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        # A Word láthatatlan vezérlőkaraktereket is tesz a szövegbe.
        t = ''.join(c for c in t if unicodedata.category(c) != 'Cf')
        t = re.sub(r'[  ]+', ' ', t).strip()
        if t:
            ki.append((javit(t), lista))
    return ki


def _cim_e(s):
    """Fejezetcím: rövid, csupa nagybetűs sor."""
    betuk = [c for c in s if c.isalpha()]
    return bool(betuk) and len(s) <= 60 and all(c.isupper() for c in betuk)


def _alcim_e(s):
    """Alcím: rövid, kettősponttal záruló sor."""
    return len(s) <= 70 and s.endswith(':') and not s.endswith('adatai:')


def szakaszok(ut):
    """[(cím, [('p'|'ul'|'alcim', tartalom), …]), …] — a dokumentum szerkezete.

    A cím előtti bevezető rész (dokumentumcím, alcím) `None` címmel jön vissza,
    hogy a hívó eldönthesse, mit kezd vele.
    """
    ki, cim, blokkok, lista = [], None, [], []

    def listat_zar():
        if lista:
            blokkok.append(('ul', list(lista)))
            lista.clear()

    for szoveg, listaelem in _bekezdesek(ut):
        if _cim_e(szoveg):
            listat_zar()
            if cim is not None or blokkok:
                ki.append((cim, blokkok))
            cim, blokkok = szoveg, []
            continue
        if listaelem:
            lista.append(szoveg)
            continue
        listat_zar()
        if _alcim_e(szoveg):
            blokkok.append(('alcim', szoveg.rstrip(':')))
        else:
            # A bekezdésen belüli sortörés önálló bekezdés a lapon: a Word
            # ezzel tagolta az adatblokkokat.
            for resz in szoveg.split('\n'):
                resz = resz.strip()
                if resz:
                    blokkok.append(('p', resz))
    listat_zar()
    if cim is not None or blokkok:
        ki.append((cim, blokkok))
    return ki


if __name__ == '__main__':
    import sys
    for ut in sys.argv[1:]:
        sz = szakaszok(pathlib.Path(ut))
        print(f'\n########## {ut}: {len(sz)} szakasz')
        for cim, blokkok in sz:
            tipusok = {}
            for t, _ in blokkok:
                tipusok[t] = tipusok.get(t, 0) + 1
            print(f'  {str(cim)[:60]:<62} {tipusok}')
