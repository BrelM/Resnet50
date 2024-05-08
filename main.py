'''
    main.py

    There will be used the saved model.

'''

from utils import load_data
from ResNet50_improved import create_model, load_weights, save_model
from keras.callbacks import EarlyStopping, ModelCheckpoint


print('\nLoading the model ...')
model = create_model()

print("\nLoading the model's weights ...")
model.set_weights(load_weights())

print('\nLoading the dataset ...')
(X_train, y_train), (X_test, y_test) = load_data()

print('\nCompiling the model ...')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print('\nTraining the model ...')

# Callbacks
filepath = "resnet50-{epoch:.2f}-loss-{loss:.2f}.keras"
checkpoint = ModelCheckpoint(filepath, monitor="val_accuracy", verbose=1, save_best_only=True, mode='min')

earlystop = EarlyStopping(monitor="val_accuracy", patience=3)
callbacks_list = [checkpoint, earlystop]

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=30, shuffle=True, callbacks=callbacks_list)

print("\nEnd of training.")

print("\nSaving...")
save_model(model)

print('\nModel saved.')

