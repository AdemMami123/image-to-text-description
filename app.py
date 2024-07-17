from flask import Flask, request, jsonify
from moondream import detect_device, LATEST_REVISION
from transformers import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
import torch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize model and tokenizer
device, dtype = detect_device()
model_id = "vikhyatk/moondream2"
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=LATEST_REVISION)
moondream = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=LATEST_REVISION, torch_dtype=dtype
).to(device=device)
moondream.eval()

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files or 'prompt' not in request.form:
        return jsonify({'error': 'Missing file or prompt'}), 400

    file = request.files['file']
    prompt = request.form['prompt']

    img = Image.open(file.stream)

    response_text = answer_question(img, prompt)

    return jsonify({'description': response_text})

def answer_question(img, prompt):
    image_embeds = moondream.encode_image(img)
    # Use the moondream model directly for question answering
    outputs = moondream.question_and_answer_pipeline(image_embeds=image_embeds, prompt=prompt)

    # Extract the generated text from the outputs
    generated_text = outputs["generated_text"]

    return generated_text

print("Starting Flask app...")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
