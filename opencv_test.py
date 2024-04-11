import cv2 as cv

from utils import load_data, REVERSED_LABELS
from ResNet50 import create_model, load_weights
from numpy import argmax, array

print('\nLoading the model ...')
model = create_model()

print("\nLoading the model's weights ...")
model.set_weights(load_weights())


face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
webcam = cv.VideoCapture(0)

def detect_bounding_box(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for (x, y, w, h) in faces:
        to_predict = array([cv.resize(img[y:y+h, x:x+w], (224, 224))])
        prediction = argmax(model.predict(to_predict))
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv.putText(img, REVERSED_LABELS[prediction], (x, y + h + 10), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 255, 0))

    return img


while True:

    result, frame = webcam.read()
    if not result:
        break # Terminate if not read successfully

    faces = detect_bounding_box(frame)
    
    cv.imshow("Real time facial recognition", faces)

    if cv.waitKey(1) and False:
        # if cv.waitKey(1) and 0xFF == ord("q"):
        break


webcam.release()
cv.destroyAllWindows()

# img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)