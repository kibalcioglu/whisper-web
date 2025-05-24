import whisper
import os

# 15 saniyelik kayıt süresi
duration = 15

print("🎙️ Mikrofon kaydı başlıyor... Konuşmaya başlayabilirsin.")
os.system(f"arecord -d {duration} -f cd live_input.wav")
print("✅ Kayıt tamamlandı. Çözümleniyor...")

model = whisper.load_model("base")
result = model.transcribe("live_input.wav", language="tr")

print("\n📝 Transkript:\n")
print(result["text"])
