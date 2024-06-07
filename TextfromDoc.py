from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
import string
import random
from pdf2image import convert_from_bytes
from driver import func
import logging
import time
import base64
from io import BytesIO
from werkzeug.datastructures import FileStorage
from prometheus_client import Counter, Histogram, generate_latest

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s]: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, filename="logs/bluebricksOCR.out")

uploaded_folder = "Images"
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
start_time = time.time()
logging.info(start_time)

if not os.path.exists(uploaded_folder):
    os.makedirs(uploaded_folder)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'App Request Count', ['endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['endpoint'])

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route("/")
def home():
    return "<h1>SMART OCR EXTRACTION </h1>"

@app.route("/TextFromDoc", methods=['POST'])
@REQUEST_LATENCY.time()
def textfromdoc():
    REQUEST_COUNT.labels(endpoint='TextFromDoc').inc()
    try:
        # print("hello")
        if 'bankName' in request.json:
            keys = request.json['bankName']
        else:
            keys = request.args.getlist('key')
        base64_string = request.json['docForOcr']
        doc_type = request.json['doc_type']
        print(doc_type)
        # Convert the base64 string to bytes
        pdf_data = base64.b64decode(base64_string)

        # Create a BytesIO object to hold the PDF data in memory
        pdf_file = BytesIO(pdf_data)

        # Create a FileStorage object
        document = FileStorage(stream=pdf_file, filename="input.pdf", content_type='application/pdf')
    except:
        # print("hello2")
        document = request.files['doc']
        doc_type = request.form.get('doc_type')
        keys = request.args.getlist('key')

    if not document:
        response = {
            "error_code": -1,
            "success": "false",
            "status": "Document not found"
        }
        return response
    filename_complete_name = secure_filename(document.filename)
    filename_front_name = filename_complete_name.split(".")[0]
    idx = len(filename_complete_name.split('.')) - 1
    filename_ext = filename_complete_name.split(".")[idx]

    if filename_ext == "pdf":
        images = convert_from_bytes(document.read())
        image_path = []
        # Save the images
        for image in images:
            filename_new_name = filename_front_name + str(id_generator()) + "." + "png"
            image.save(os.path.join(uploaded_folder, filename_new_name))
            img_path = os.path.join(uploaded_folder, filename_new_name)
            image_path.append(img_path)
    else:
        filename_new_name = filename_front_name + str(id_generator()) + "." + filename_ext
        document.save(os.path.join(uploaded_folder, filename_new_name))
        image_path = [os.path.join(uploaded_folder, filename_new_name)]

    data = func(image_path, keys, doc_type)
    end_time = time.time()
    logging.info(end_time)
    elapsed_time = end_time - start_time
    logging.info(elapsed_time)
    return data

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
