import os
import argparse
from services.slides_to_images import export_slides_to_images, extract_slide_texts
from services.tts import synthesize_narrations
from services.video import build_video_from_slides

def main():
    parser = argparse.ArgumentParser(description="Convert PPTX to narrated video.")
    parser.add_argument("pptx", help="Path to input .pptx")
    parser.add_argument("--out", default="output.mp4", help="Path to output .mp4")
    parser.add_argument("--workdir", default="workdir", help="Intermediate work directory")
    args = parser.parse_args()

    os.makedirs(args.workdir, exist_ok=True)

    slide_texts = extract_slide_texts(args.pptx)

    images_dir = os.path.join(args.workdir, "images")
    os.makedirs(images_dir, exist_ok=True)
    image_paths = export_slides_to_images(args.pptx, images_dir)

    audio_dir = os.path.join(args.workdir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    audio_paths = synthesize_narrations(slide_texts, audio_dir)

    build_video_from_slides(image_paths, audio_paths, args.out)
    print(f"Done: {args.out}")

if __name__ == "__main__":
    main()
