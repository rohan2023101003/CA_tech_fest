from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
from allocation import allocate_rooms

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        group_file = request.files['groupFile']
        hostel_file = request.files['hostelFile']
        
        group_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'group_info.csv')
        hostel_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'hostel_info.csv')
        
        group_file.save(group_file_path)
        hostel_file.save(hostel_file_path)
        
        results = allocate_rooms(group_file_path, hostel_file_path)
        
        return render_template('result.html', results=results)
    return render_template('upload.html')

@app.route('/download')
def download():
    return send_file('uploads/allocation_result.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
