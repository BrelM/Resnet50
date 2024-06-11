import cv2 as cv
from PIL import Image
from utils import load_data, REVERSED_LABELS
from ResNet50_improved import create_model, load_weights
from numpy import argmax, array, asarray

import os
import base64
from flask import Flask, request
from flask_json import FlaskJSON, json_response



print('\nLoading the model ...')
model = create_model()

print("\nLoading the model's weights ...")
#model.set_weights(load_weights())
model=load_weights()


face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_bounding_box(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=4, minSize=(150, 150))

    try:
        for (x, y, w, h) in faces:
            to_predict = array([cv.resize(img[y:y+h, x:x+w], (224, 224))])
            prediction = argmax(model.predict(to_predict, verbose=0))
            
            
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv.putText(img, REVERSED_LABELS[prediction], (x, y + h + 10), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0))
        
            
        response = REVERSED_LABELS[prediction]
    
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

        to_send = cv.imread("images/" + image.filename)
        label_, labeled_image = detect_bounding_box(to_send)
        
        to_return = Image.fromarray(labeled_image)
        to_return = base64.b64encode(to_return.tobytes()).decode()
        
        # to_return.show()
        # cv.imshow("ezez", cv.resize(labeled_image, (700, 1000)))
        # cv.waitKey(0)   
        # cv.destroyAllWindows()
        
        # return send_file("images/" + image.filename)


        return json_response(label=label_, image=to_return, size=labeled_image.shape)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

