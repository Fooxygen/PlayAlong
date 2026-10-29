import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "web" / "assets" / "fonts"

ASCII = {chr(code) for code in range(32, 127)}
PUNCT = set("，。！？；：、“”‘’（）【】《》…—·￥")

CJK = set()
for high in range(0xB0, 0xF8):
    for low in range(0xA1, 0xFF):
        try:
            CJK.add(bytes([high, low]).decode("gb2312"))
        except UnicodeDecodeError:
            pass

TEXT = set()
for path in [
    ROOT / "web" / "index.html",
    *sorted((ROOT / "cases" / "json").glob("*.json")),
]:
    TEXT.update(path.read_text(encoding="utf-8"))


def available_chars(path: Path) -> set[str]:
    font = TTFont(path, lazy=True)
    codepoints = set()
    for table in font["cmap"].tables:
        codepoints.update(table.cmap.keys())
    font.close()
    return {chr(code) for code in codepoints}


def build(source: Path, target: Path, requested: set[str], features: list[str]) -> None:
    chars = sorted(ch for ch in requested if ch in available_chars(source))

    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = features
    options.name_IDs = ["*"]
    options.notdef_outline = True
    options.recalc_bounds = True
    options.drop_tables += ["DSIG"]

    font = subset.load_font(str(source), options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text="".join(chars))
    subsetter.subset(font)
    subset.save_font(font, str(target), options)
    font.close()

    print(
        f"{source.name} -> {target.name}: "
        f"{len(chars)} chars, "
        f"{source.stat().st_size / 1024 / 1024:.1f} MB -> "
        f"{target.stat().st_size / 1024 / 1024:.1f} MB"
    )


only = sys.argv[1] if len(sys.argv) > 1 else ""

if only in ("", "keinann"):
    source = FONT_DIR / "keinann" / "KeinannMaruPOP.ttf"
    if source.exists():
        build(
            source,
            FONT_DIR / "keinann" / "Keinann-subset.woff2",
            ASCII | PUNCT | CJK | TEXT,
            ["kern"],
        )
    else:
        print("skip KeinannMaruPOP.ttf: source missing")

if only in ("", "quicksand"):
    build(
        FONT_DIR / "quicksand" / "Quicksand-Variable.ttf",
        FONT_DIR / "quicksand" / "Quicksand-subset.woff2",
        ASCII | PUNCT,
        ["kern"],
    )
