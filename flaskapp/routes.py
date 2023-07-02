from flask import Flask, render_template, request, send_from_directory
from flaskapp import app
from flaskapp.facerec import detect_faces, faiss_knn, rindex_knn
import os                                       # send images that aren't in static       
import base64                                   # encode uploaded images
import time                                     # query time

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_pic():
    if 'file' not in request.files:
        return 'No file uploaded.'
    
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return 'No file selected.'

        img = file.read()

        try:
            numeric_value = int(request.form.get('numeric', 5))
        except ValueError:
            numeric_value = 5

        start_time = time.perf_counter()

        results, names, similarity_scores, best_result = rindex_knn(img, numeric_value)
        
        total_time = time.perf_counter() - start_time
        print(total_time)
        zipped_data = zip(results, names, similarity_scores)

        img_base64 = base64.b64encode(img).decode('utf-8')
        return render_template('results.html', data=zipped_data, best_result_image=best_result, original_image=img_base64, time=(total_time))

# Retrieve an image outside the static folder for the frontend
@app.route('/dataset/<path:filename>')
def serve_image(filename):
    dataset_dir = os.path.join(os.getcwd(), 'dataset')
    return send_from_directory(dataset_dir, filename)