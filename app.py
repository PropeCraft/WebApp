from flask import Flask, request, jsonify, render_template
from pathlib import Path
import hashlib
import google.generativeai as genai
from flask_cors import CORS  # Import the CORS module
import os
from werkzeug.utils import secure_filename
from flask import session

app = Flask(__name__)
app.secret_key = 'myflask'  # Set your secret key here
CORS(app)  # Use the CORS module to enable CORS for all routes

genai.configure(api_key="AIzaSyA1E1lphv2Za_iD93LGV3H63LxEwmeX0j8")

# Set up the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_instruction = "Deeply Analyze the image and give the recommendations of sustainable and ecofriendly decorative or makeover ideas "

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    system_instruction=system_instruction,
    safety_settings=safety_settings,
)

uploaded_files = []

def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No selected image"}), 400
    basepath = os.path.dirname(__file__)
    image_path = os.path.join(basepath, 'uploads', secure_filename(image_file.filename))
    image_file.save(image_path)
    session['image_path'] = image_path
    return jsonify({"image_path": image_path})

@app.route('/makeover_recommendations', methods=['POST'])
def makeover_recommendations():
    image_path = session.get('image_path')

    prompt_parts = [
        *upload_if_needed(image_path),
        "Analyze the image and suggest some sustainable and eco friendly interior design or decorative visualizations as per the space",
    ]
    response = model.generate_content(prompt_parts)
    recommendations = response.text
    for uploaded_file in uploaded_files:
        genai.delete_file(name=uploaded_file.name)
    return jsonify({"recommendations": recommendations})

@app.route('/balcony_recommendations', methods=['POST'])
def balcony_recommendations():
    image_path = request.json['image_path']
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = genai.Image(content=content)
    prompt_parts = [
        *upload_if_needed(image_path),
        "Analyze the image and suggest some sustainable and eco friendly balcony makeover visualizations as per the space",
    ]
    response = model.generate_content(prompt_parts)
    recommendations = response.text
    for uploaded_file in uploaded_files:
        genai.delete_file(name=uploaded_file.name)
    return jsonify({"recommendations": recommendations})

@app.route('/painting_recommendations', methods=['POST'])
def painting_recommendations():
    image_path = request.json['image_path']
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = genai.Image(content=content)
    prompt_parts = [
        *upload_if_needed(image_path),
        "Analyze the image and suggest sustainable and eco friendly aesthetic  or beautiful wall or colour paints ",
    ]
    response = model.generate_content(prompt_parts)
    recommendations = response.text
    for uploaded_file in uploaded_files:
        genai.delete_file(name=uploaded_file.name)
    return jsonify({"recommendations": recommendations})

@app.route('/gardening_recommendations', methods=['POST'])
def gardening_recommendations():
    image_path = request.json['image_path']
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = genai.Image(content=content)
    prompt_parts = [
        *upload_if_needed(image_path),
        "Analyze the image and suggest some sustainable and eco friendly gardening makeover visualizations as per the space",
    ]
    response = model.generate_content(prompt_parts)
    recommendations = response.text
    for uploaded_file in uploaded_files:
        genai.delete_file(name=uploaded_file.name)
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
