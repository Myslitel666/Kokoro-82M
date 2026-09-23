from pathlib import Path
from kokoro import KPipeline
import numpy as np
import subprocess
import os

# --------------------------------------------------
# Настройки
# --------------------------------------------------

TEXT_FILE = "text.txt"
OUTPUT_FILE = "kokoro_full.mp3"

VOICE = "af_heart"
SPEED = 1.0

# --------------------------------------------------
# Читаем текст
# --------------------------------------------------

text = Path(TEXT_FILE).read_text(encoding="utf-8").strip()

if not text:
    raise ValueError("text.txt пустой")

# --------------------------------------------------
# Сначала считаем ТОЧНОЕ количество чанков
# Без загрузки модели и без генерации аудио
# --------------------------------------------------

counter = KPipeline(
    lang_code="a",
    model=False
)

chunks = list(counter(text))

total_chunks = len(chunks)

print(f"Всего чанков: {total_chunks}")

# --------------------------------------------------
# Настоящий pipeline
# --------------------------------------------------

pipeline = KPipeline(
    lang_code="a"
)

generator = pipeline(
    text,
    voice=VOICE,
    speed=SPEED
)

# --------------------------------------------------
# ffmpeg -> один MP3
# --------------------------------------------------

ffmpeg = subprocess.Popen(
    [
        "ffmpeg",
        "-y",
        "-f", "f32le",
        "-ar", "24000",
        "-ac", "1",
        "-i", "pipe:0",
        "-c:a", "libmp3lame",
        "-b:a", "128k",
        OUTPUT_FILE,
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.PIPE,
)

# --------------------------------------------------
# Генерация
# --------------------------------------------------

for i, (_, _, audio) in enumerate(generator, start=1):

    if audio is None:
        continue

    audio = np.asarray(audio, dtype=np.float32)

    ffmpeg.stdin.write(audio.tobytes())
    ffmpeg.stdin.flush()

    print(f"Generated chunk {i}/{total_chunks}")

# --------------------------------------------------
# Завершение ffmpeg
# --------------------------------------------------

ffmpeg.stdin.close()

stderr = ffmpeg.stderr.read().decode("utf-8", errors="ignore")
return_code = ffmpeg.wait()

if return_code != 0:
    raise RuntimeError(stderr)

if not os.path.isfile(OUTPUT_FILE):
    raise RuntimeError("MP3 не создан")

print(f"Saved: {OUTPUT_FILE}")
print(f"Size: {os.path.getsize(OUTPUT_FILE) / 1024 / 1024:.2f} MB")