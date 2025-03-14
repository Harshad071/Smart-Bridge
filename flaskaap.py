from flask import Flask, render_template, Response, jsonify, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerRangeField
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired
import cv2
import numpy as np
from hubconfCustom import video_detection
from hubconfcustomweb import video_detection_web
from lane import process_frame
import os

app = Flask(__name__)

# We are styling our application using the Bootstrap Library
Bootstrap(app)

# Here we have configured a secret key
app.config['SECRET_KEY'] = 'muhammadmoin'

app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    conf_slide = IntegerRangeField('Confidence:  ', default=25, validators=[InputRequired()])
    submit = SubmitField("Run")

frames = 0
sizeImage = 0
detectedObjects = 0

def generate_combined_frames(path_x='', conf_=0.25):
    # Open video file
    cap = cv2.VideoCapture(path_x)
    if not cap.isOpened():
        print("Error opening video stream or file.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.")
            break

        # Perform video detection
        yolo_output = video_detection(path_x, conf_)
        for detection_, FPS_, xl, yl in yolo_output:
            ref, buffer = cv2.imencode('.jpg', detection_)
            global frames
            frames = str(FPS_)
            global sizeImage
            sizeImage = str(xl[0])
            global detectedObjects
            detectedObjects = str(yl)

            # Perform lane detection on the frame
            final_output = process_frame(frame)

            if final_output is None:
                print("No output from process_frame.")
                continue

            # Overlay video detection results onto lane detection
            combined_output = cv2.addWeighted(final_output, 0.3, detection_, 0.5, 0)
            
            _, jpeg = cv2.imencode('.jpg', combined_output)
            frame_bytes = jpeg.tobytes()

            # Send combined frame to the client
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('indexproject.html')

@app.route("/lane_detection", methods=['GET', 'POST'])
def lane_vedio():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        conf_ = form.conf_slide.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        session['conf_'] = conf_
    return render_template('ui2.html', form=form)



@app.route('/FrontPage', methods=['GET', 'POST'])
def front():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        conf_ = form.conf_slide.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        session['conf_'] = conf_
    return render_template('videoprojectnew.html', form=form)

@app.route('/video')
def video():
    return Response(generate_combined_frames(path_x=session.get('video_path', None),
                                             conf_=round(float(session.get('conf_', None)) / 100, 2)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/lane')
def lane():
    video_path = session.get('video_path', None)
    if not video_path:
        return "No video file found in session", 400
    return Response(generate_combined_frames(path_x=video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fpsgenerate', methods=['GET'])
def fps_fun():
    global frames
    return jsonify(result=frames)

@app.route('/sizegenerate', methods=['GET'])
def size_fun():
    global sizeImage
    return jsonify(imageSize=sizeImage)

@app.route('/detectionCount', methods=['GET'])
def detect_fun():
    global detectedObjects
    return jsonify(detectCount=detectedObjects)

if __name__ == "__main__":
    app.run(debug=True)
