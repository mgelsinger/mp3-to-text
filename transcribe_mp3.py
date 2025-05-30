#!/usr/bin/env python3
"""transcribe_mp3.py — Command‑line batch MP3 → text transcription using OpenAI Whisper.

Features
--------
* Accepts one or more MP3 files **or** directories (recurses for *.mp3).
* Streams audio straight to Whisper—no manual conversion needed (ffmpeg must be installed).
* Saves a UTF‑8 `.txt` file next to each MP3 (same basename).
* Handles GPU or CPU automatically (override with --device).
* Lets you pick any Whisper model size with --model; defaults to 'base'.
* Prints a neat progress log.

Example
-------
$ python transcribe_mp3.py podcast1.mp3 lectures/ --model medium --device cuda:0

Dependencies
------------
pip install -U openai-whisper  # installs torch automatically
# System‑wide FFmpeg is required for decoding (https://ffmpeg.org)

"""

from __future__ import annotations
import argparse
import pathlib
import sys
import shutil

import torch
import whisper


def collect_mp3s(paths: list[str]) -> list[pathlib.Path]:
    """Expand files and directories into a flat list of MP3 Path objects."""
    mp3s: list[pathlib.Path] = []
    for raw in paths:
        p = pathlib.Path(raw).expanduser().resolve()
        if p.is_dir():
            mp3s.extend(sorted(p.rglob("*.mp3")))
        elif p.suffix.lower() == ".mp3" and p.is_file():
            mp3s.append(p)
        else:
            print(f"⚠️  Skipping '{raw}' (not an MP3 or directory)", file=sys.stderr)
    return mp3s


def transcribe(mp3: pathlib.Path, model: whisper.Whisper) -> str:
    """Run Whisper and return plain‑text transcription."""
    result = model.transcribe(str(mp3), fp16=model.device.type != "cpu")
    return result["text"].strip()


def main() -> None:
    if not shutil.which("ffmpeg"):
        sys.exit("Error: FFmpeg binary not found in PATH. Install FFmpeg first.")

    parser = argparse.ArgumentParser(
        description="Batch‑transcribe MP3 files to plain‑text using OpenAI Whisper."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="One or more .mp3 files or directories containing .mp3 files",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="base",
        help="Whisper model size (tiny, base, small, medium, large). Default: base",
    )
    parser.add_argument(
        "-d",
        "--device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Device string for PyTorch (e.g. 'cpu', 'cuda', 'cuda:0')",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .txt files (default: skip)",
    )
    args = parser.parse_args()

    print(f"Loading Whisper model '{args.model}' on {args.device}…")
    model = whisper.load_model(args.model, device=args.device)

    mp3_paths = collect_mp3s(args.inputs)
    if not mp3_paths:
        sys.exit("No MP3 files found.")

    for mp3 in mp3_paths:
        out_txt = mp3.with_suffix(".txt")
        if out_txt.exists() and not args.overwrite:
            print(f"⏭  {out_txt.name} already exists — skipping. (Use --overwrite to redo)")
            continue

        print(f"🎤  Transcribing {mp3.name} …", end=" ", flush=True)
        try:
            text = transcribe(mp3, model)
            out_txt.write_text(text, encoding="utf‑8")
            print("✔")
        except Exception as e:
            print("✖", e, file=sys.stderr)


if __name__ == "__main__":
    main()
