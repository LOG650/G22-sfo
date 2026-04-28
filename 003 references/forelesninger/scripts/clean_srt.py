"""SRT -> ren tekst. Fjerner tidsstempler, segment-numre, disclaimer, og slår sammen til avsnitt."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw_srt"
OUT = ROOT / "clean_txt"
OUT.mkdir(exist_ok=True)

DISCLAIMER = "[Auto-generated transcript. Edits may have been applied for clarity.]"
TIME_RE = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\s*$")
NUM_RE = re.compile(r"^\d+\s*$")


def srt_to_text(srt: str) -> str:
    lines = srt.splitlines()
    chunks: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s or NUM_RE.match(s) or TIME_RE.match(s):
            continue
        s = s.replace(DISCLAIMER, "").strip()
        if s:
            chunks.append(s)
    text = " ".join(chunks)
    text = re.sub(r"\s+", " ", text).strip()
    # Avsnitt-skift på lange pauser markert med flere punktum eller etter ~600 tegn ved punktum
    paragraphs: list[str] = []
    buf: list[str] = []
    count = 0
    for sent in re.split(r"(?<=[.!?])\s+", text):
        buf.append(sent)
        count += len(sent)
        if count > 700:
            paragraphs.append(" ".join(buf))
            buf = []
            count = 0
    if buf:
        paragraphs.append(" ".join(buf))
    return "\n\n".join(paragraphs)


def main() -> None:
    rows: list[tuple[str, int, int]] = []
    for srt_path in sorted(RAW.glob("*.srt")):
        text = srt_to_text(srt_path.read_text(encoding="utf-8"))
        out_path = OUT / (srt_path.stem + ".txt")
        out_path.write_text(text, encoding="utf-8")
        rows.append((srt_path.stem, len(text), text.count(" ") + 1))
    print(f"Skrev {len(rows)} renset filer til {OUT}")
    # Indeks
    idx = ["# Forelesningsindeks (auto-transkripsjon, renset)\n"]
    idx.append("| Dato | Økt | Tittel | Tegn | Ord (ca.) |")
    idx.append("|---|---|---|---:|---:|")
    for stem, chars, words in rows:
        m = re.match(r"(\d{4}-\d{2}-\d{2})_okt(\d)_(.+)", stem)
        if m:
            date, okt, title = m.group(1), m.group(2), m.group(3).replace("_", " ")
        else:
            date, okt, title = "?", "?", stem
        idx.append(f"| {date} | {okt} | {title} | {chars:,} | {words:,} |")
    (ROOT / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(f"Indeks: {ROOT / 'INDEX.md'}")


if __name__ == "__main__":
    main()
