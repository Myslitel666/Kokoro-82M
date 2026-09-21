from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code="a")

text = """
Hello! This is a test of Kokoro text to speech running locally
on an Intel Core i9 processor without a dedicated GPU.
"""

generator = pipeline(
    text,
    voice="af_heart",
    speed=1.0
)

for i, (_, _, audio) in enumerate(generator):
    filename = f"kokoro_{i}.wav"
    sf.write(filename, audio, 24000)
    print(f"Saved: {filename}")