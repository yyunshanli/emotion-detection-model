from flask import Flask, request, jsonify, render_template
import base64
import cv2
import numpy as np
import os
from webcam_recognition_helper_functions import js_to_image, bbox_to_bytes  # Ensure this module exists

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        image_data = data['image']  # Expecting base64 string from frontend

        # Convert base64 to OpenCV image
        img = js_to_image(image_data)

        # Check if image conversion was successful
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400

        # Save the image to a file
        image_path = os.path.join(os.getcwd(), 'captured_image.jpg')
        if not cv2.imwrite(image_path, img):
            return jsonify({'error': 'Failed to save image'}), 500

        # Process the image (e.g., apply bounding boxes)
        img_with_bbox = img  # Replace this with your actual processing logic

        # Convert the processed image back to base64
        bbox_bytes = bbox_to_bytes(img_with_bbox)

        return jsonify({'bbox_image': bbox_bytes})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)