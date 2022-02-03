# from distutils.log import debug
from flask import Flask, flash, request, redirect, url_for, render_template
# import urllib.request
import os
from werkzeug.utils import secure_filename
  
import psycopg2 
import psycopg2.extras
     
app = Flask(__name__)
#App config
app.secret_key = "uploadSecretkey"
     
DB_HOST = "127.0.0.1"
DB_NAME = "sampledb"
DB_USER = "moringa"
DB_PASS = "root"
     
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

UPLOAD_FOLDER = 'static/uploads/'
  
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @TODO: Create a default htmlPage      
@app.route('/')
def home():
    return render_template('index.html')

# @TODO: Create upload image route 
@app.route('/', methods=['POST'])
def upload_image():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Select Image for upload')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #Save a duplicate on local directory after upload
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 
        cursor.execute("INSERT INTO upload (title) VALUES (%s)", (filename,))
        conn.commit()
 
        flash('UPLOADED IMAGE BELOW')
        return render_template('index.html', filename=filename)
    else:
        flash('! IMAGE FORMATS ONLY ALLOWED are - PNG, JPG, JPEG, GIF')
        return redirect(request.url)
  
# @TODO: Create a display image route 
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
  
if __name__ == "__main__":
    app.run(debug=True)
