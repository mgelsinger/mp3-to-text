# 🎤 transcribe_mp3.py

Batch-transcribe any collection of **MP3** files to plain-text using [OpenAI Whisper](https://github.com/openai/whisper).  
Drop it in a folder of podcasts, lectures, or voice notes and get a `.txt` file next to every track—no manual audio conversion needed.

|                        |                                           |
|------------------------|-------------------------------------------|
| **Language**           | Python 3.8 – 3.12                         |
| **Dependencies**       | `openai-whisper` (incl. PyTorch) · FFmpeg |
| **License**            | MIT                                       |
| **Author**             | *Your Name*                               |
| **Latest release**     | See [Changelog](#-changelog)              |

---

## ✨ Features

* **One‑liner install** (`pip install -U openai-whisper`) – everything else is pure Python.  
* Works with **individual files *or* folders** (recursive search for `*.mp3`).  
* Saves clean UTF‑8 transcripts (`podcast_episode.mp3 → podcast_episode.txt`).  
* Automatic CPU/GPU pick‑up — or override with `--device cuda:0`.  
* Choose any Whisper checkpoint (`tiny`, `base`, `small`, `medium`, `large`) via `--model`.  
* Friendly progress log and graceful skipping of already‑transcribed files.  
* Zero temp files; streams audio straight through FFmpeg.

---

## 🚀 Quick start

```bash
# 1  (Optional) inside a project folder
python -m venv venv
source venv/bin/activate            # Windows: venv\\Scripts\\activate

# 2  Install dependencies
pip install -U openai-whisper       # pulls in torch + friends
# GPU users: install the CUDA wheel for torch instead (see below).

# 3  Put the script in this folder
curl -O https://raw.githubusercontent.com/yourname/transcribe-mp3/main/transcribe_mp3.py

# 4  Transcribe!
python transcribe_mp3.py lectures/ --model medium --device cuda:0
```

> **Heads‑up (Windows):** make sure FFmpeg is in your `PATH`.  
> The quickest way is `choco install ffmpeg` or unzip the official build and add the `bin` folder to `PATH`.

---

## 🛠 Command‑line options

| Flag | Default | Description |
|------|---------|-------------|
| `inputs…`        | _(required)_ | One or more `.mp3` files **or** directories. |
| `-m, --model`    | `base`      | Whisper checkpoint (`tiny` → `large`). |
| `-d, --device`   | `cuda` if available else `cpu` | Any PyTorch device string (`cpu`, `cuda:1`, etc.). |
| `--overwrite`    | _(false)_   | Re‑transcribe even if the `.txt` file already exists. |

Example:

```bash
python transcribe_mp3.py podcasts/*.mp3 --model small --device cpu --overwrite
```

---

## ⚡️ GPU install (optional but ≈ 5× faster)

```bash
pip uninstall torch torchaudio torchvision -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Match the CUDA version (`cu121`, `cu118`, …) to your local toolkit / driver.

---

## 📂 Project structure

```text
transcribe-mp3/
├─ transcribe_mp3.py        ▶ main script
├─ requirements.txt         ▶ pinned deps (optional)
└─ README.md                ▶ this file
```

Feel free to rename or move **transcribe_mp3.py**; it has no hard‑coded paths.

---

## ❓ FAQ

**Why MP3 only?**  
Whisper accepts many formats, but MP3 is the common denominator.  
If you want universal intake just change `*.mp3` to `*.*` inside `collect_mp3s()`.

**Can I get SRT / VTT subtitles?**  
Yes—replace the call to `result["text"]` with `whisper.utils.get_writer("srt")`, or open an issue and we’ll add `--format srt`.

**Does it work on macOS M‑series?**  
Yep—PyTorch’s Metal backend kicks in automatically (`device mps`).

---

## 🤝 Contributing

1. **Fork & clone** the repo  
2. **Create a branch** `git checkout -b feat/my-awesome-idea`  
3. _(Optional)_ `pre-commit install` for hooks  
4. **Submit a PR** — tests and docs welcome!

---

## 📜 License

MIT © 2025 *Your Name*.  
OpenAI Whisper is licensed under the MIT License (see upstream repo).

---

## 🗒 Changelog

### v1.0.0  (2025‑05‑30)
* First public release 🎉
