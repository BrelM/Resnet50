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


LABELS = {
    "Brel":0,
    "Anselme":1,
    "Rafiatou":2
}


# LABELS = {
#     "brad":0,
#     "dicaprio":1,
#     "jolie":2
# }

REVERSED_LABELS = {_[0]:_[1] for _ in [(value, key) for key, value in LABELS.items()]}

# def load_my_model(fpath:str="./base_model.keras") -> Model:
    
#     return load_model("fpath")



def load(dir:str, shape:tuple=(224,224, 3)) -> tuple:

    # Loading dataset
    data = []
    labels = []

    dir_content = os.listdir(dir)

    for _ in dir_content:
        file = Image.open(os.path.join(dir, _)) # .resize((shape[0], shape[1]))

        temp_file = np.asarray(file)
        if file.size == (224, 224):
            file = temp_file
        else:
            file = file.resize((shape[0], shape[1]))
            file.save(os.path.join(dir, _))
            file = temp_file.reshape((1, shape[0], shape[1], shape[2]))

        # Adding the file
        data.append(file)
        
        # Adding the label
        for key in LABELS.keys():
            if key in _:
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