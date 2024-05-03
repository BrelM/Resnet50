import cv2 as cv
import sys


name = sys.argv[1]

train_data_path = "dataset/train_data/"

face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
webcam = cv.VideoCapture(0)

def save_bounding_box(img, index):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for (x, y, w, h) in faces:
        cv.imwrite(
           train_data_path + name + str(index) + ".png",
            cv.resize(img[y:y+h, x:x+w], (224, 224))
        )
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        
    return img



while True:
    index = 100
    for _ in range(index):
        result, frame = webcam.read()
        if not result:
            break # Terminate if not read successfully

        faces = save_bounding_box(frame, index - _)
        
        cv.imshow("Real time facial recognition", faces)

        if cv.waitKey(1) and 0xFF == ord("q"):
            break

webcam.release()
cv.destroyAllWindows()
