from ResNet50_improved import load_weights
from keras.models import Model
from keras.layers import Flatten

model = load_weights()


output = None

for layer in model.layers:
    if isinstance(layer, Flatten):
        output = layer.output


if layer:
    new_model = Model(inputs=model.input, outputs=output)

    new_model.save("FExtractor.keras")
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print(new_model.summary())
