from flask import Flask, render_template, Response
import cv2
import os

app = Flask(__name__)

# Initialize the webcam
cap = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_image', methods=['POST'])
def capture_image():
    success, frame = cap.read()
    if success:
        # Save the image
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, frame)
        return {'status': 'success', 'path': image_path}
    return {'status': 'error'}

if __name__ == '__main__':
    app.run(debug=True)


