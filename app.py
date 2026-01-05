import os
import whisper
from moviepy.video.io.VideoFileClip import VideoFileClip
from openai import OpenAI
from dotenv import load_dotenv

# ✅ IMPORTANT: Set OPENAI_API_KEY as environment variable
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔹 STEP 1: English → Spoken Tanglish (STRICT STYLE)
def english_to_tanglish(english_text):
    prompt = f"""
You are converting English content into NATURAL, SPOKEN TANGlish
used by Tamil speakers in Instagram reels and webinars.

STRICT RULES (DO NOT BREAK):
- English letters only (NO Tamil script)
- Casual spoken Tamil style
- Keep meaning EXACT
- Keep SAME order of ideas
- Short sentences
- NOT formal
- NOT explanation tone
- NOT rewritten English
- Use breaks exactly like spoken pauses

### EXAMPLE (FOLLOW THIS STYLE EXACTLY)

English:
Even if you look at it, AI is based on machine learning.
But do you know the number one high demand job in India? Data science.

Tanglish:
Paathaalum AI machine learning base-la dhaan irukku.
Aana India-la number one high demand job enna nu theriyuma?
Adhu Data Science.

---

English:
Only knowing coding is not enough.
You should know how to make business decisions using data.

Tanglish:
Summa coding mattum therinja podhaadhu.
Data use panni business decision epdi edukuradhu nu theriyanum.

---

NOW CONVERT THE BELOW CONTENT
USING THE SAME STYLE, FLOW & STRUCTURE

English:
{english_text}

Tanglish Output:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You strictly follow the Tanglish style shown in examples."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.15
    )

    return response.choices[0].message.content.strip()


# 🔹 STEP 2: Video → English → Tanglish
def video_to_tanglish(video_path):
    print("🎬 Processing started...")

    audio_path = "temp_audio.wav"

    # 1️⃣ Extract audio
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)

    # 2️⃣ Whisper → English (BEST POSSIBLE)
    model = whisper.load_model("small")  # use "medium" if system allows
    result = model.transcribe(
        audio_path,
        language="en",
        task="transcribe",
        temperature=0,
        fp16=False,
        condition_on_previous_text=False
    )

    english_text = result["text"]

    print("\n🟡 ENGLISH TRANSCRIPT:\n")
    print(english_text)

    # 3️⃣ English → Tanglish
    tanglish_text = english_to_tanglish(english_text)

    # 4️⃣ Save output
    with open("tanglish_output.txt", "w", encoding="utf-8") as f:
        f.write(tanglish_text)

    os.remove(audio_path)

    print("\n🔥 FINAL TANGlish OUTPUT:\n")
    print(tanglish_text)
    print("\n✅ Saved as tanglish_output.txt")


# ▶️ RUN FROM HERE (ONLY ONE ENTRY POINT)
if __name__ == "__main__":
    video_to_tanglish("insta_video.mp4")
