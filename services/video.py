import os
from typing import List
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips




MIN_SLIDE_DURATION = 3.0  # seconds

def build_video_from_slides(image_paths: List[str], audio_paths: List[str], out_path: str) -> None:
    assert len(image_paths) == len(audio_paths), "Number of images and audio files must match."
    clips = []
    for img, aud in zip(image_paths, audio_paths):
        audio = AudioFileClip(aud)
        duration = max(audio.duration, MIN_SLIDE_DURATION)
        clip = ImageClip(img, duration=duration).set_audio(audio)

        clips.append(clip)
    final = concatenate_videoclips(clips, method="chain")
    # Ensure FPS is reasonable for still images
    final.write_videofile(out_path, fps=24, codec="libx264", audio_codec="aac")
    for c in clips:
        c.close()
    final.close()
