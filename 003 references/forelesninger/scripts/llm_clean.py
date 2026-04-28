"""LLM-rens av ASR-transkripsjon med per-chunk caching.

Hver chunk lagres separat under cleaned_llm/.chunks/<filnavn-stem>/<idx>.txt
Slik at re-kjøring bare prosesserer manglende chunks.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "clean_txt"
DST = ROOT / "cleaned_llm"
CACHE = DST / ".chunks"
DST.mkdir(exist_ok=True)
CACHE.mkdir(exist_ok=True)

# Last .env
ENV_FILE = ROOT / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

CHUNK_CHARS = 9_000
API_URL = "https://api.anthropic.com/v1/messages"
MODEL_ALIAS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-7",
}

SYSTEM_PROMPT = """Du renser auto-transkriberte norske forelesninger fra LOG650 (Forskningsprosjekt: Logistikk og kunstig intelligens) ved Høgskolen i Molde. Forelesningene dekker bl.a.: kvantitative metoder (lineær programmering, ABC-analyse, sensitivitetsanalyse, EOQ/økonomisk ordrestørrelse), forskningsdesign, kapittelstruktur for vitenskapelig rapport, KI i logistikk, programmering, databehandling, og APA 7-referanser.

Auto-transkripsjonen har mye norsk ASR-rusk: dialektord blir feiltranskribert, fagtermer skrives feil, setninger brytes rart. Eksempler: "Bur reine" = "være ren/være rett", "PhD i hode" = "passe inn der", "k i" eller "Kodi" eller "kj" = "KI" (kunstig intelligens), "AD" = "område", "Pre-modern" = "Problemstilling" eller "Modell", "Q1" = "Q*" (optimal ordrestørrelse), "Cody" = "Koding", "Belgia" = "bedrifta".

Din oppgave: skriv om utdraget til lesbar, sammenhengende norsk prosa. Behold *all* meningsbærende informasjon — ingenting skal kuttes.

Regler:
1. Fiks ASR-feil basert på kontekst. Foretrekk fagtermen som gir mening framfor lydlikhet.
2. Slå sammen oppstykkede setninger til naturlige setninger.
3. Behold første-persons tale og uformell tone der det passer — ikke gjør om til formell akademisk tekst.
4. Fyll inn småord (og, så, det, å) som ASR har droppet, men *ikke* finn på nytt innhold.
5. Hvis et parti er helt uforståelig, marker med [uklart] heller enn å gjette vilt.
6. Behold avsnittsstrukturen omtrent som original.

Returner KUN den rensede teksten. Ingen forklaring, ingen meta-kommentar, ingen overskrifter, ingen kodeblokker."""


def chunk_text(text: str, size: int) -> list[str]:
    if len(text) <= size:
        return [text]
    parts: list[str] = []
    i = 0
    while i < len(text):
        end = min(i + size, len(text))
        if end < len(text):
            br = text.rfind("\n\n", i, end)
            if br > i + size // 2:
                end = br
        parts.append(text[i:end].strip())
        i = end
    return parts


def call_api(chunk: str, model: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY ikke satt")
    body = {
        "model": MODEL_ALIAS.get(model, model),
        "max_tokens": 8000,
        "system": [
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "messages": [
            {"role": "user", "content": f"UTDRAG TIL RENSING:\n---\n{chunk}\n---"}
        ],
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    delay = 5
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            return payload["content"][0]["text"].strip()
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()[:300]
            if e.code == 429:
                print(f"    [429 retry om {delay}s] {err_body[:120]}", flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 180)
                continue
            raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
        except Exception as e:
            print(f"    [retry om {delay}s] {e}", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 180)
    raise RuntimeError("oppga etter 6 forsøk")


def get_chunk(file_stem: str, idx: int, chunk: str, model: str) -> str:
    """Returner cached eller hent fra API."""
    cache_dir = CACHE / file_stem
    cache_dir.mkdir(exist_ok=True)
    cf = cache_dir / f"{idx:03d}.txt"
    if cf.exists() and cf.stat().st_size > 0:
        return cf.read_text(encoding="utf-8")
    cleaned = call_api(chunk, model)
    cf.write_text(cleaned, encoding="utf-8")
    return cleaned


def process_file(src: Path, model: str) -> tuple[str, str]:
    dst = DST / src.name
    if dst.exists() and dst.stat().st_size > 0:
        return (src.name, "hopp over (finnes)")
    text = src.read_text(encoding="utf-8")
    chunks = chunk_text(text, CHUNK_CHARS)
    out_parts: list[str] = []
    t0 = time.time()
    for i, chunk in enumerate(chunks, 1):
        try:
            cleaned = get_chunk(src.stem, i, chunk, model)
        except Exception as e:
            return (src.name, f"FEIL chunk {i}: {e}")
        out_parts.append(cleaned)
    dst.write_text("\n\n".join(out_parts), encoding="utf-8")
    elapsed = time.time() - t0
    return (src.name, f"ok ({elapsed:.0f}s, {len(chunks)} chunks, {dst.stat().st_size:,} B)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--only", help="substring-match")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()

    files = sorted(SRC.glob("*.txt"))
    if args.only:
        files = [f for f in files if args.only.lower() in f.name.lower()]
    if args.limit:
        files = files[: args.limit]
    print(f"LLM-rens: {len(files)} fil(er), modell={args.model}, workers={args.workers}", flush=True)
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(process_file, f, args.model): f for f in files}
        for fut in concurrent.futures.as_completed(futs):
            name, status = fut.result()
            print(f"  [{status}] {name}", flush=True)
    print(f"Ferdig på {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
