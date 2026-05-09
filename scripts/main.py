import argparse
import json
import os
import sys
from pathlib import Path

# Allow `python scripts/main.py` from repo root
sys.path.insert(0, str(Path(__file__).parent))

from config import DEFAULT_OUT, DEFAULT_TEMPLATE, FONT_FAMILY_PLACEHOLDER, PLACEHOLDER_MAP
from fetcher import fetch_player
from parser import parse_player
from renderer import render


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Generate Clash Royale stat card SVG")
    ap.add_argument("--tag", default=os.environ.get("CR_TAG"), help="Player tag (with or without #)")
    ap.add_argument("--token", default=os.environ.get("CR_TOKEN"), help="CR API bearer token")
    ap.add_argument("--font", default=os.environ.get("CR_FONT"), help="Absolute path to .otf font file")
    ap.add_argument("--template", default=os.environ.get("CR_TEMPLATE", DEFAULT_TEMPLATE), help="SVG template path")
    ap.add_argument("--out", default=os.environ.get("CR_OUT", DEFAULT_OUT), help="Output SVG path")
    ap.add_argument("--dry-run", action="store_true", help="Print parsed data and exit without rendering")
    return ap


def main() -> None:
    ap = build_parser()
    args = ap.parse_args()

    if not args.tag:
        ap.error("--tag or CR_TAG is required")
    if not args.token:
        ap.error("--token or CR_TOKEN is required")

    raw = fetch_player(args.tag, args.token)
    parsed = parse_player(raw)

    if args.dry_run:
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
        return

    if not args.font:
        ap.error("--font or CR_FONT is required for rendering")

    font_abs = str(Path(args.font).resolve())
    render(
        parsed=parsed,
        template_path=args.template,
        font_path=font_abs,
        out_path=args.out,
        placeholder_map=PLACEHOLDER_MAP,
        placeholder_family=FONT_FAMILY_PLACEHOLDER,
    )
    print(f"Written → {args.out}")


if __name__ == "__main__":
    main()
