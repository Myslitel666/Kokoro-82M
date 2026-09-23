from pathlib import Path
from kokoro import KPipeline
import soundfile as sf
import numpy as np

pipeline = KPipeline(lang_code="a")

text = Path("text.txt").read_text(encoding="utf-8")

generator = pipeline(
    text,
    voice="af_heart",
    speed=1.0
)

audio_chunks = []

for i, (_, _, audio) in enumerate(generator):
    audio_chunks.append(audio)
    print(f"Generated chunk {i + 1}")

# Объединяем все куски
full_audio = np.concatenate(audio_chunks)

# Сохраняем один итоговый WAV
sf.write("kokoro_full.wav", full_audio, 24000)

print("Saved: kokoro_full.wav")