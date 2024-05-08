'''
    utils.py

    A set of useful functions for loading and preprocessing the dataset.

'''

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from keras.models import load_model, Model
from keras.utils import to_categorical
from PIL import Image
import numpy as np
import cv2 as cv




LABELS = {
    "Brel":0,
    "Anselme":1,
    "Emaha":2
}


# LABELS = {
#     "brad":0,
#     "dicaprio":1,
#     "jolie":2
# }

REVERSED_LABELS = {_[0]:_[1] for _ in [(value, key) for key, value in LABELS.items()]}

# def load_my_model(fpath:str="./base_model.keras") -> Model:
    
#     return load_model("fpath")


face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

def save_bounding_box(img:Image.Image, path:str, shape:tuple):
    
    img_mat = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    gray_img = cv.cvtColor(img_mat, cv.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    faces_to_return = []
    root_pos = path.rfind('.')
    index = 0
    for (x, y, w, h) in faces:

        to_save = cv.resize(img_mat[y:y+h, x:x+w], shape)

        cv.imwrite(
           path[:root_pos] + str(index) + path[root_pos:],
           to_save
        )
        index += 1

        faces_to_return.append(Image.fromarray(cv.cvtColor(to_save, cv.COLOR_BGR2RGB)))

    return faces_to_return




def load(dir:str, shape:tuple=(224,224)) -> tuple:

    # Loading dataset
    data = []
    labels = []

    dir_content = os.listdir(dir)

    for _ in dir_content:
        
        if '.' in _: # If _ is actually a file

            file = Image.open(os.path.join(dir, _))

            # If the loaded image doesn't meet the shape standards (maybe not cropped yet) we do so,
            # save the cropped version before adding to the dataset
            if file.size != shape:
                # faces is a list consisting of Image objects of all the faces extrated in the current file 
                faces = save_bounding_box(file, os.path.join(dir, _), shape)

                # Adding the face(s)
                for f in faces:

                    data.append(np.asarray(f))
                
                    # Adding the label
                    for key in LABELS.keys():
                        if key in _:
                            labels.append(LABELS[key])
                            break

                # Moving the old parent image
                os.system("mkdir " + os.path.join(dir, "old_images").replace('/', '\\'))
                os.system("move " + os.path.join(dir, _) + " " + os.path.join(os.path.join(dir, "old_images"), _).replace('/', '\\'))

            else:
                
                # Adding the file
                data.append(np.asarray(file))
                
                # Adding the label
                for key in LABELS.keys():
                    if key.lower() in _.lower():
                        labels.append(LABELS[key])
                        break


    return np.array(data), to_categorical(labels)


def load_data(path:str="./dataset") -> tuple:

    train_data_path = os.path.join(path, "train_data")
    test_data_path = os.path.join(path, "test_data")

    # Loading training dataset
    train_data = load(train_data_path)
    # Loading training dataset
    test_data = load(test_data_path)

    return train_data, test_data