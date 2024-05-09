'''
    test.py

    There will be used tested the traied model.

'''

from utils import load_data, REVERSED_LABELS
from ResNet50_improved import create_model, load_weights
from numpy import argmax

print('\nLoading the model ...')
model = create_model()

print("\nLoading the model's weights ...")
model.set_weights(load_weights())

print('\nLoading the dataset ...')
(X_train, y_train), (X_test, y_test) = load_data()

predictions = model.predict(X_test)

predictions = argmax(predictions, axis=1)
true_labels = argmax(y_test, axis=1)

for _ in range(len(predictions)):
    print(REVERSED_LABELS[predictions[_]], REVERSED_LABELS[true_labels[_]])

del model


