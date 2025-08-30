import os
from typing import List
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

def _narration_for(text: str) -> str:
    # You can enhance this to summarize / rephrase with an LLM if desired.
    return text if text.strip() else "This slide contains no text."

def _try_elevenlabs(text: str, out_path: str) -> bool:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return False
    try:
        from elevenlabs import ElevenLabs
        voice = os.getenv("ELEVENLABS_VOICE_ID", "Rachel")
        client = ElevenLabs(api_key=api_key)
        audio = client.generate(text=_narration_for(text), voice=voice, model="eleven_multilingual_v2")
        with open(out_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        return True
    except Exception:
        return False

def synthesize_narrations(slide_texts: List[str], out_dir: str) -> List[str]:
    os.makedirs(out_dir, exist_ok=True)
    audio_paths = []
    for idx, text in enumerate(slide_texts, start=1):
        out_mp3 = os.path.join(out_dir, f"slide_{idx:03d}.mp3")
        # Prefer ElevenLabs if configured
        if not _try_elevenlabs(text, out_mp3):
            # Fallback to gTTS (free)
            tts = gTTS(_narration_for(text), lang="en")
            tts.save(out_mp3)
        audio_paths.append(out_mp3)
    return audio_paths
