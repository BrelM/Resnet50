'''
    main.py

    There will be used the saved model.

'''

from utils import load_data, load_my_model
from ResNet50 import create_model, load_weights, save_model


print('Loading the model ...')
model = create_model()

print("Loading the model's weights ...")
model.set_weights(load_weights())

print('Loading the dataset ...')
(X_train, y_train), (X_test, y_test) = load_data()

print('Compiling the model ...')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print('Training the model ...')
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, shuffle=True)

print("End of training.")

print("Saving...")
save_model(model)

print('Model saved.')