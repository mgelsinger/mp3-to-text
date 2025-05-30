# 🎤 transcribe_mp3.py

Batch-transcribe any collection of **MP3** files to plain-text using [OpenAI Whisper](https://github.com/openai/whisper).  
Drop it in a folder of podcasts, lectures, or voice notes and get a `.txt` file next to every track—no manual audio conversion needed.

|                        | |
|------------------------|----------------------------------------------------------------|
| **Language**           | Python 3.8 – 3.12 |
| **Dependencies**       | `openai-whisper` (inc. PyTorch) · system FFmpeg |
| **License**            | MIT |
| **Author**             | *Your name* |
| **Latest release**     | See [CHANGELOG](#-changelog) |

---

## ✨ Features

* **One-liner install** (`pip install -U openai-whisper`) – everything else is pure Python.  
* Works with **individual files _or_ folders** (recursive search for `*.mp3`).  
* Saves clean UTF-8 transcripts (`podcast_episode.mp3 → podcast_episode.txt`).  
* Automatic CPU/GPU pick-up — or override with `--device cuda:0`.  
* Choose any Whisper checkpoint (`tiny`, `base`, `small`, `medium`, `large`) via `--model`.  
* Friendly progress log and graceful skipping of already-transcribed files.  
* Zero temp files; streams audio straight through FFmpeg.

---

## 🚀 Quick start

```bash
# 1  (Optional) inside a project folder
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate

# 2  Install dependencies
pip install -U openai-whisper       # pulls in torch + friends
# GPU users: install the CUDA wheel for torch instead (see below).

# 3  Put the script in this folder
curl -O https://raw.githubusercontent.com/yourname/transcribe-mp3/main/transcribe_mp3.py

# 4  Transcribe!
python transcribe_mp3.py lectures/ --model medium --device cuda:0
