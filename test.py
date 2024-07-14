'''
    test.py

    There will be used tested the traied model.

'''

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from keras.models import load_model
from utils import load_data, REVERSED_LABELS
from ResNet50_improved import create_model, load_weights
from numpy import argmax, array
from sklearn.metrics import accuracy_score, precision_score, recall_score,f1_score 


print('\nLoading the model ...')
# model = create_model()

print("\nLoading the model's weights ...")
# model.set_weights(load_weights())
model = load_model("base_model.keras")

print('\nLoading the dataset ...')
(X_train, y_train), (X_test, y_test) = load_data()


# Testing
print('\nTesting ...')
predictions = model.predict(X_test, verbose=1)

# predictions = argmax(predictions, axis=1)
y_pred = argmax(predictions, axis=1)
y_test = argmax(y_test, axis=1)

print(y_test.shape, y_pred.shape)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

print('Accuracy: {:2f}%\n\
Precision : {:2f}%\n\
Recall : {:2f}%\n\
F1-score : {:2f}%'.format(accuracy*100, precision*100, recall*100, f1*100))



# for _ in range(len(predictions)):
#     print(REVERSED_LABELS[predictions[_]], REVERSED_LABELS[true_labels[_]])




