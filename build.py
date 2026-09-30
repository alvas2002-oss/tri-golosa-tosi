#!/usr/bin/env python3
"""Build the standalone public copy of the lesson from the working source.

Source of truth: /root/tosya-academy/work/lessons/ (page fragment + audio clips).
The fragment has no <html>/<head>/<body>; this script wraps it, drops the temporary
"for the adult" voice-audition block, and copies only the clips the lesson plays.
"""
import shutil
from pathlib import Path

SRC = Path("/root/tosya-academy/work/lessons")
OUT = Path(__file__).parent

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<meta name="description" content="Игровой урок русского языка для 2 класса: повествовательные, вопросительные и побудительные предложения с кошкой Тосей.">
<style>body{margin:0} img{max-width:100%} [hidden]{display:none!important}</style>
"""

page = (SRC / "tri-golosa-tosi.html").read_text(encoding="utf-8")
start = page.index('    <div class="panel"><span class="count">ДЛЯ ВЗРОСЛОГО')
end = page.index("</div></div>`; }", start) + len("</div></div>")
page = page[:start].rstrip() + page[end:]
assert "ДЛЯ ВЗРОСЛОГО" not in page

style_end = page.index("</style>") + len("</style>")
html = HEAD + page[:style_end] + "\n</head>\n<body>\n" + page[style_end:] + "\n</body>\n</html>\n"
(OUT / "index.html").write_text(html, encoding="utf-8")

audio = OUT / "audio"
shutil.rmtree(audio, ignore_errors=True)
audio.mkdir()
clips = [f for f in sorted((SRC / "audio").glob("*.mp3")) if not f.name.startswith(("voice_", "kid_"))]
for f in clips:
    shutil.copy(f, audio / f.name)
(OUT / ".nojekyll").write_text("")
print(f"index.html: {len(html)} bytes, clips: {len(clips)}")
