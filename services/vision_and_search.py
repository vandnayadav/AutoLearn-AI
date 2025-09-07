import os
import requests
from typing import List, Optional

# Try to import a transformers-based captioner if available
try:
    from transformers import pipeline
    _caption_pipeline = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
except Exception:
    _caption_pipeline = None

# Optional OpenAI polishing
try:
    import openai
except Exception:
    openai = None

DUCKDUCKGO_API = "https://api.duckduckgo.com"

def caption_image(image_path: str) -> str:
    if _caption_pipeline is None:
        return f"An image from slide: {os.path.basename(image_path)}"
    try:
        captions = _caption_pipeline(image_path, max_new_tokens=64)
        if isinstance(captions, list) and captions:
            return captions[0].get('generated_text') or captions[0].get('caption') or str(captions[0])
        return str(captions)
    except Exception:
        return f"An image from slide: {os.path.basename(image_path)}"

def search_web_duckduckgo(query: str, max_results: int = 3) -> List[str]:
    try:
        r = requests.get(DUCKDUCKGO_API, params={ "q": query, "format": "json", "no_html": 1, "skip_disambig": 1 }, timeout=10)
        r.raise_for_status()
        j = r.json()
        snippets = []
        if j.get("AbstractText"):
            snippets.append(j["AbstractText"])
        for t in j.get("RelatedTopics", [])[:max_results]:
            text = t.get("Text") or (t.get("Topics")[0].get("Text") if t.get("Topics") else None)
            if text:
                snippets.append(text)
            if len(snippets) >= max_results:
                break
        return snippets[:max_results]
    except Exception:
        return []

def polish_with_openai(raw_text: str, api_key_env: str = "OPENAI_API_KEY") -> Optional[str]:
    api_key = os.getenv(api_key_env)
    if not api_key or openai is None:
        return None
    try:
        openai.api_key = api_key
        resp = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are an assistant that writes clear slide explanations for presentations."},
                {"role": "user", "content": raw_text}
            ],
            max_tokens=400,
            temperature=0.2
        )
        choice = resp["choices"][0]["message"]["content"]
        return choice.strip()
    except Exception:
        return None

def analyze_and_explain(image_path: str) -> str:
    caption = caption_image(image_path)
    web_snippets = search_web_duckduckgo(caption, max_results=3)
    parts = [f"Caption: {caption}."]
    if web_snippets:
        parts.append("Relevant web information:")
        for s in web_snippets:
            parts.append(f"- {s}")
    raw = "\\n".join(parts)
    polished = polish_with_openai(raw)
    if polished:
        return polished
    text = caption + ". "
    if web_snippets:
        text += "Context from the web: " + "; ".join(web_snippets)
    return text