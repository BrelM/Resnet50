'''
    main.py

    There will be used the saved model.

'''

from utils import load_data
from ResNet50_improved import create_model, load_weights, save_model
from keras.callbacks import EarlyStopping


print('\nLoading the model ...')
model = create_model()

print("\nLoading the model's weights ...")
model.set_weights(load_weights())

print('\nLoading the dataset ...')
(X_train, y_train), (X_test, y_test) = load_data()

print('\nCompiling the model ...')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print('\nTraining the model ...')
callback = EarlyStopping(monitor="val_accuracy", patience=1)
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=30, shuffle=True, callbacks=[callback])

print("\nEnd of training.")

print("\nSaving...")
save_model(model)

print('\nModel saved.')

