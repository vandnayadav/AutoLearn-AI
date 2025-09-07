const generateForm = document.querySelector(".generate-form");
const generateBtn = generateForm.querySelector(".generate-btn");
const promptInput = document.querySelector(".prompt-input");
const imageGallery = document.querySelector(".image-gallery");

const KEY = "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";  // Replace with your Hugging Face token
const HF_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0";

let isImageGenerating = false;

const updateImageCard = (srcUrl) => {
  const imgCard = document.querySelector(".img-card");
  const imgElement = imgCard.querySelector("img");
  const downloadBtn = imgCard.querySelector(".download-btn");

  imgElement.src = srcUrl;

  imgElement.onload = () => {
    imgCard.classList.remove("loading");
    downloadBtn.setAttribute("href", srcUrl);
    downloadBtn.setAttribute("download", `${promptInput.value}.jpg`);
  };
};

async function query() {
  const response = await fetch(HF_MODEL_URL, {
    headers: {
      Authorization: `Bearer ${KEY}`,
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({ inputs: promptInput.value }),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error || "Failed to generate image");
  }

  return await response.blob();
}

const generateAiImages = async () => {
  try {
    const response = await query();
    const objectURL = URL.createObjectURL(response);
    updateImageCard(objectURL);
  } catch (error) {
    alert("Image generation failed: " + error.message);
  } finally {
    generateBtn.removeAttribute("disabled");
    generateBtn.innerText = "Generate";
    isImageGenerating = false;
  }
};

const handleImageGeneration = (e) => {
  e.preventDefault();
  if (isImageGenerating) return;

  generateBtn.setAttribute("disabled", true);
  generateBtn.innerText = "Generating...";
  isImageGenerating = true;

  const imgCardMarkup = `
    <div class="img-card loading">
      <img   src="{{ url_for('static', filename='images\download.svg')}}" alt="AI generated image">
      <a class="download-btn" href="#">
        <img src="images/download.svg" alt="download icon">
      </a>
    </div>`;

  imageGallery.innerHTML = imgCardMarkup;
  generateAiImages();
};

generateForm.addEventListener("submit", handleImageGeneration);
