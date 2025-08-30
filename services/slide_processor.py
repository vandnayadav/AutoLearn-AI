import os
from typing import List
from services.slides_to_images import extract_slide_texts
from services.vision_and_search import analyze_and_explain

TEXT_MIN_LENGTH = 15  # threshold for using extracted text

def generate_slide_explanations(pptx_path: str, slide_image_paths: List[str]) -> List[str]:
    slide_texts = extract_slide_texts(pptx_path)
    explanations = []
    for idx, img_path in enumerate(slide_image_paths):
        txt = slide_texts[idx] if idx < len(slide_texts) else ""
        if txt and len(txt.strip()) >= TEXT_MIN_LENGTH:
            explanations.append(txt.strip())
        else:
            print(f"[slide_processor] Analyzing image for slide {idx+1}: {img_path}")
            expl = analyze_and_explain(img_path)
            explanations.append(expl)
    return explanations