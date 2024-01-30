import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = os.getcwd() + '/static/images' # Get current working directory & add /static/images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    images = []
    for fn in os.listdir(UPLOAD_FOLDER):
        if fn.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
            images.append(fn)
    return render_template('index.html', images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        
        file = request.files["file"]
        
        if file.filename == "":
            return "No selected file", 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            return redirect(url_for('index'))
    
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)

