'''
    main.py

    There will be used the saved model.

'''

from utils import load_data, TimingCallback
from keras.models import load_model
from ResNet50_improved import create_model, load_weights, save_model
from keras.callbacks import EarlyStopping, ModelCheckpoint


print('\nLoading the model ...')
# model = create_model()

print("\nLoading the model's weights ...")
# model.set_weights(load_weights())
model = load_model('base_model.keras')

print('\nLoading the dataset ...')
(X_train, y_train), (X_test, y_test) = load_data()

print('\nCompiling the model ...')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print('\nTraining the model ...')

# Callbacks
timer = TimingCallback()
filepath = "resnet50-{epoch}-loss-{loss:.2f}-accuracy-{accuracy:.2f}-val_accuracy-{val_accuracy:.2f}.keras"
checkpoint = ModelCheckpoint(filepath, monitor="accuracy", verbose=1, save_best_only=True, mode='max')
checkpoint1 = ModelCheckpoint(filepath, monitor="val_accuracy", verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor="val_accuracy", patience=10)


callbacks_list = [checkpoint, checkpoint1, timer, earlystop]

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, shuffle=True, callbacks=callbacks_list)

print(f"\nEnd of training.\nThe training lasted: {sum(timer.logs)} s.")

print("\nSaving...")
save_model(model)

print('\nModel saved.')

