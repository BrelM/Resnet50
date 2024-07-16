import cv2 as cv
from PIL import Image
from utils import load_data, REVERSED_LABELS
from numpy import argmax, array
from keras.models import load_model
# from ResNet50_improved import create_model, load_weights
# from keras.layers import Dense

import os
import base64
from flask import Flask, request
from flask_json import FlaskJSON, json_response



print('\nLoading the model ...')
print("\nLoading the model's weights ...")
model = load_model("FExtractor.keras")
#model.set_weights(load_weights())
# model = load_weights()

# # Freezig Dense layers
# for layer in model.layers:
#     if isinstance(layer, Dense):
#         layer.trainable = False



face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_bounding_box(img:cv.Mat):

    # Resizing output image if too big. This is just in case the image is to big to be previewed
    ratio = 0.2
    if img.shape[0] > 400 and img.shape[1] > 600:
        img = cv.resize(img, (int(img.shape[1] * ratio), int(img.shape[0] * ratio)))

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=4, minSize=(150, 150))

    try:
        for (x, y, w, h) in faces:
            to_predict = array([cv.resize(img[y:y+h, x:x+w], (224, 224))])
            
            # Characteristics vector
            prediction = model.predict(to_predict, verbose=0)
            
        response = prediction
    
    except:
        response = "The individual could not be recognised"

    return response, cv.cvtColor(img, cv.COLOR_BGR2RGB)





# create folder for uploaded data
FOLDER = '.'
os.makedirs(FOLDER, exist_ok=True)

app = Flask(__name__)
FlaskJSON(app)

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
        image.save("images/" + image.filename)

        image = cv.imread("images/" + image.filename)
        char_vector, image = detect_bounding_box(image)

        image = Image.fromarray(image)
        size = image.size
        image = base64.b64encode(image.tobytes()).decode()
        
        if not isinstance(char_vector, str):
            char_vector = char_vector.tolist()

        return json_response(vector=char_vector, image=image, size=size)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

