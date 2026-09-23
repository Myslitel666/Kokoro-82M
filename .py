pipeline = KPipeline(lang_code="a")

text = Path("text.txt").read_text(encoding="utf-8") # Читаем текст из файла text.txt

generator = pipeline(
    text,
    voice="af_heart",
    speed=1.0
)

for i, (_, _, audio) in enumerate(generator):
    filename = f"kokoro_{i}.wav"
    sf.write(filename, audio, 24000)