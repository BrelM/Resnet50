import cv2 as cv

from utils import load_data, REVERSED_LABELS
from ResNet50 import create_model, load_weights
from numpy import argmax, array, frombuffer

import os
from flask import Flask, request, send_from_directory




face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_bounding_box(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for (x, y, w, h) in faces:
        to_predict = array([cv.resize(img[y:y+h, x:x+w], (224, 224))])
        prediction = argmax(model.predict(to_predict))
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv.putText(img, REVERSED_LABELS[prediction], (x, y + h + 10), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0))

    return REVERSED_LABELS[prediction], img


# create folder for uploaded data
FOLDER = '.'
os.makedirs(FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        message = '''<form action="" method="POST"><select name="file">'''
        files = os.listdir()
        files.sort()
        for _ in files:
            if os.path.isfile(_):
                message += f'''<option value="{_}">{_[:30]}</option>'''

        message += '''</select><input type="submit" value="Download"/></form>'''

        return message
    
    
    if request.method == 'POST':
        
        image = request.files.get('image')
        # image.save(image.filename)

        label, labeled_image = detect_bounding_box(frombuffer(image))

        return label



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    
    print('\nLoading the model ...')
    model = create_model()

    print("\nLoading the model's weights ...")
    model.set_weights(load_weights())

