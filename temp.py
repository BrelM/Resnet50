
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from keras.models import load_model
from keras.models import Model
from keras.layers import Flatten

model = load_model("base_model.keras")


output = None

for layer in model.layers:
    if isinstance(layer, Flatten):
        output = layer.output



if output != None:
    new_model = Model(inputs=model.input, outputs=output)

    new_model.save("FExtractor.keras")
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print(new_model.summary())
