#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:08:03 2024

@author: nevase
"""


from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, session
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "You Will Never Guess"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# image classification function
def detect_object(uploaded_image_path):
    # Loading image
    img = cv2.imread(uploaded_image_path)

 
    # # Defining desired shape
    fWidth = 540
    fHeight = 540
 
    # Resize image in opencv
    img = cv2.resize(img, (fWidth, fHeight))
 
    height, width, channels = img.shape
    
    class_p = 'SK'
    prob = 0.94
    
    # Write output image (object detection output)
    cv2.imwrite(uploaded_image_path, img)
 
    out_class = "The prediction is: {} With a confidence of: {}".format(class_p, prob)
    return(out_class)
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        # flash('Image successfully uploaded and displayed below')
        class_pred = detect_object(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # predicted_json ={"filename":filename, "Class 0":"Text 0", "Class 1":"Text 1"}
        return render_template('index.html', filename=filename, predicted_text=class_pred)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()