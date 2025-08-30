from flask import Flask, render_template, request, redirect, session
import pymysql
import os
import uuid
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from services.slides_to_images import export_slides_to_images, extract_slide_texts
from services.tts import synthesize_narrations
from services.video import build_video_from_slides
from services.slide_processor import generate_slide_explanations

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'Vandana'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')




load_dotenv()

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
OUTPUT_DIR = os.path.join(os.getcwd(), "outputs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)



ALLOWED_EXT = {".pptx"}

@app.route("/ppt_to_video", methods=["GET", "POST"])
def ppt_to_video():
    if request.method == "POST":
        if "pptx" not in request.files:
            flash("No file part")
            return redirect(url_for("ppt_to_video"))
        f = request.files["pptx"]
        if f.filename == "":
            flash("No selected file")
            return redirect(url_for("ppt_to_video"))
        _, ext = os.path.splitext(f.filename)
        if ext.lower() not in ALLOWED_EXT:
            flash("Upload a .pptx file")
            return redirect(url_for("ppt_to_video"))

        job_id = str(uuid.uuid4())[:8]
        workdir = os.path.join(OUTPUT_DIR, job_id)
        os.makedirs(workdir, exist_ok=True)
        pptx_path = os.path.join(UPLOAD_DIR, secure_filename(f.filename))
        f.save(pptx_path)

        # 1) Extract text per slide
        slide_texts = extract_slide_texts(pptx_path)

        # 2) Export slide images
        images_dir = os.path.join(workdir, "images")
        os.makedirs(images_dir, exist_ok=True)
        exported_paths = export_slides_to_images(pptx_path, images_dir)

        # 3) Synthesize narration files (mp3 per slide)
        audio_dir = os.path.join(workdir, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        audio_paths = synthesize_narrations(slide_texts, audio_dir)

        # 4) Build final video
        out_video = os.path.join(workdir, "output.mp4")
        build_video_from_slides(exported_paths, audio_paths, out_video)

        return redirect(url_for("result", job_id=job_id))
    return render_template("ppt_to_video.html")

@app.route("/result/<job_id>")
def result(job_id):
    out_path = os.path.join(OUTPUT_DIR, job_id, "output.mp4")
    if not os.path.exists(out_path):
        flash("Result not found")
        return redirect(url_for("ppt_to_video"))
    return render_template("ppt_result.html", job_id=job_id)

@app.route("/download/<job_id>")
def download(job_id):
    out_path = os.path.join(OUTPUT_DIR, job_id, "output.mp4")
    return send_file(out_path, as_attachment=True, download_name=f"ppt2video_{job_id}.mp4")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Enable Debug Mode
