'''
    utils.py

    A set of useful functions for loading and preprocessing the dataset.

'''

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from keras.models import load_model
from keras.utils import to_categorical
from PIL import Image
import numpy as np

LABELS = {
    "brad":0,
    "jolie":1,
    "dicaprio":2
}

def load_model(fpath:str="./base_model.keras"):
    
    return load_model("fpath")



def load(dir:str, shape:tuple=(224,224, 3)):

    # Loading dataset
    data = []
    labels = []

    dir_content = os.listdir(dir)

    for _ in dir_content:
        file = Image.open(os.path.join(dir, _)).resize((shape[0], shape[1]))

        temp_file = np.asarray(file)
        if file.size == (224, 224):
            file.save(os.path.join(dir, _))
            file = temp_file
        else:
            file = temp_file.reshape((1, shape[0], shape[1], shape[2]))

        # Adding the file
        data.append(file)
        
        # Adding the label
        for key in LABELS.keys():
            if key in _:
                labels.append(LABELS[key])
                break
    
    return np.array(data), to_categorical(labels)


def load_data(path:str="./dataset"):

    train_data_path = os.path.join(path, "train_data")
    test_data_path = os.path.join(path, "test_data")

    # Loading training dataset
    train_data = load(train_data_path)
    # Loading training dataset
    test_data = load(test_data_path)

    return train_data, test_data