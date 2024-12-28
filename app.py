from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
from rembg import remove
from PIL import Image
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Remove background
        with open(filepath, 'rb') as input_file:
            img = Image.open(input_file)
            img = img.convert("RGBA")
            output = remove(img)

        output_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        with open(output_path, 'wb') as output_file:
            output.save(output_file, format='PNG')

        return redirect(url_for('processed', filename=filename))

@app.route('/processed/<filename>')
def processed(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return render_template('processed.html', filename=filename, file_path=file_path)

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

