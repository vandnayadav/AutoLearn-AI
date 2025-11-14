# AutoLearn-AI
📌 About the Project

AutoLearn-AI is an educational automation tool built using Python + Flask.
It integrates multiple AI APIs like YouTube Data API v3 and Hugging Face API, along with automation libraries such as yt-dlp, MoviePy, and python-pptx.

It is designed to make learning easy by providing:
✔ AI search
✔ AI content creation
✔ Automated downloading
✔ Automatic slide generation
✔ Automatic flowchart creation

🎯 Features
🔍 YouTube Video Search (Best Quality Results)

Uses YouTube Data API v3
Fetches videos based on topic
Sorts results by view count
Displays top 4 best videos
Fast and reliable search

🎨 AI Image Generation (Hugging Face API)

Enter any text prompt
Generates high-quality AI images
Uses modern text-to-image models
Helpful for presentations & creative tasks

📥 Universal Video Downloader

Supports:
✔ YouTube
✔ Instagram
✔ Facebook
✔ Twitter/X
✔ TikTok
✔ Reddit

Powered by yt-dlp, which downloads videos in the best available quality.

📊 Video to PPT Converter

Upload video or paste URL

Extracts 1 frame per second

Converts frames into a PowerPoint file

Useful for teaching, notes, and documentation

Libraries used:
MoviePy, Pillow, python-pptx

🔄 Flowchart Creator from Pseudocode

Enter pseudocode

AI recognizes steps, decisions, loops

Automatically generates a clean flowchart

Great for programming & algorithm learning

🛠️ Tech Stack

Backend: Python, Flask
APIs: YouTube Data API v3, Hugging Face API
Libraries: yt-dlp, MoviePy, python-pptx, instaloader, Pillow
Frontend: HTML, CSS, Bootstrap, JavaScript (AJAX)

AutoLearn-AI/
│── app.py
│── templates/
│── static/
│── uploads/
│── downloads/
│── services/
│── requirements.txt
│── README.md


🚀 How to Run the Project
1️⃣ Clone repository
git clone https://github.com/yourusername/AutoLearn-AI.git
cd AutoLearn-AI

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add API keys

Create a .env file

YOUTUBE_API_KEY=your_api_key
HF_TOKEN=your_huggingface_key

4️⃣ Run the app
python app.py


📌 Future Improvements

Local Stable Diffusion support

AI video summarization

Automatic PPT narration generator

Add user login & cloud storage
