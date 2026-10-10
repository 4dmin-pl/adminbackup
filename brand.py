"""AdminBackup: nakłada markę A.D.M.I.N na rozpakowane pliki oficjalnego klienta UrBackup.

Użycie:  python brand.py klient <staging> <brand_out>
           python brand.py serwer <katalog_www>
  staging     - katalog z plikami klienta (z `msiexec /a`), nadpisywany: ikony statusu, logo1.png, tłumaczenia, info.txt
  brand_out   - tu trafiają bitmapy instalatora WiX (WixUIDialogBmp.bmp, WixUIBannerBmp.bmp)
  katalog_www - logo i favicon panelu serwera (wkładane do obrazu Docker przez serwer/Dockerfile)
Wymaga: pip install pillow resvg-py polib
"""
import io
import sys
from pathlib import Path

import polib
import resvg_py
from PIL import Image, ImageDraw

SRC = Path(__file__).resolve().parent / "grafika"
TLO = (33, 40, 48, 255)  # granat z ikonka_logo.svg (jak AdminDesk)
NAZWA = "AdminBackup"
# kolor plakietki statusu w rogu ikony zasobnika
STATUSY = {
    "backup-ok": (46, 160, 67),
    "backup-bad": (218, 54, 51),
    "backup-progress": (31, 111, 235),
    "backup-progress-pause": (139, 148, 158),
    "backup-no-server": (110, 118, 129),
    "backup-indexing": (163, 113, 247),
    "backup-no-recent": (227, 160, 8),
}
ICO = [16, 24, 32, 48, 128, 256]


def render(svg, width):
    png = resvg_py.svg_to_bytes(svg_path=str(SRC / svg), width=width)
    im = Image.open(io.BytesIO(bytes(png))).convert("RGBA")
    return im.crop(im.getbbox())


def biale(im):
    out = Image.new("RGBA", im.size, (255, 255, 255, 255))
    out.putalpha(im.getchannel("A"))
    return out


def ikona(size=256, plakietka=None):
    """Białe „A” na zaokrąglonym granacie; opcjonalnie kolorowa kropka statusu w prawym dolnym rogu."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=size // 5, fill=TLO)
    znak = biale(render("znak.svg", size))
    znak.thumbnail((int(size * 0.68), int(size * 0.68)), Image.LANCZOS)
    im.alpha_composite(znak, ((size - znak.width) // 2, (size - znak.height) // 2))
    if plakietka:
        r = int(size * 0.24)
        c = size - r - int(size * 0.04)
        d.ellipse((c - r, c - r, c + r, c + r), fill=plakietka + (255,), outline=(255, 255, 255, 255), width=max(1, size // 32))
    return im


def wix_bitmapy(out):
    out.mkdir(parents=True, exist_ok=True)
    dlg = Image.new("RGB", (493, 312), (255, 255, 255))  # lewy pas 164 px na grafikę, reszta na tekst WiX
    dlg.paste(TLO[:3], (0, 0, 164, 312))
    ik = ikona(120)
    dlg.paste(ik, ((164 - 120) // 2, 60), ik)
    dlg.save(out / "WixUIDialogBmp.bmp")
    ban = Image.new("RGB", (493, 58), (255, 255, 255))  # tekst WiX po lewej, ikona po prawej
    ik = ikona(46)
    ban.paste(ik, (493 - 46 - 8, 6), ik)
    ban.save(out / "WixUIBannerBmp.bmp")


def tlumaczenia(staging):
    n = 0
    for mo_path in staging.glob("lang/*/urbackup.mo"):
        mo = polib.mofile(str(mo_path))
        for e in mo:
            if "UrBackup" in e.msgstr:
                e.msgstr = e.msgstr.replace("UrBackup", NAZWA)
                n += 1
        mo.save(str(mo_path))
    return n


def main(staging, brand_out):
    staging, brand_out = Path(staging), Path(brand_out)
    for nazwa, kolor in STATUSY.items():
        ikona(256, kolor).save(staging / f"{nazwa}.ico", format="ICO", sizes=[(s, s) for s in ICO])
    logo = Image.new("RGBA", (100, 91), (0, 0, 0, 0))  # rozmiar jak oryginalne logo1.png
    logo.alpha_composite(ikona(91), (4, 0))
    logo.save(staging / "logo1.png")
    wix_bitmapy(brand_out)
    n = tlumaczenia(staging)
    info = staging / "info.txt"
    info.write_text(
        f"{NAZWA} - kopie zapasowe A.D.M.I.N (4dmin.pl), by Karol Wojewski.\n"
        "Oparte na UrBackup (AGPL v3+); zmiany marki: https://github.com/4dmin-pl/adminbackup\n\n"
        + info.read_text(encoding="utf-8-sig"),
        encoding="utf-8-sig",
    )
    assert all((staging / f"{k}.ico").stat().st_size > 0 for k in STATUSY)
    print(f"OK: 7 ikon statusu, logo1.png, bitmapy WiX, {n} tekstów w tłumaczeniach")


def serwer(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    ikona(40).save(out / "urbackup.png")  # nazwa i rozmiar jak w oryginalnym panelu (images/urbackup.png)
    ikona(256).save(out / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"OK: logo i favicon panelu w {out}")


if __name__ == "__main__":
    if sys.argv[1] == "serwer":
        serwer(sys.argv[2])
    else:
        main(*sys.argv[2:4])
