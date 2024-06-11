import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"


import pickle
# import keras
from keras import Model
from keras.models import load_model
from keras.layers import Input, Conv2D, BatchNormalization, Activation, Add, ZeroPadding2D, MaxPooling2D, AveragePooling2D, Dense, Flatten
from keras.initializers import glorot_uniform



#Implementation of convolution block
def convolutional_block(X, f, filters, stage, block, s):
    
    F1, F2, F3 = filters
    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(1, 1), padding='valid', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F2, kernel_size=(f, f), strides=(1, 1), padding='same', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), padding='valid', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)

    return X



#Implementation of Identity Block

def identity_block(X, f, filters, stage, block):

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'
    F1, F2, F3 = filters

    X_shortcut = X

    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=conv_name_base + '2a', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2a')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F2, kernel_size=(f, f), strides=(1, 1), padding='same', name=conv_name_base + '2b', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=conv_name_base + '2c', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2c')(X)

    # Skip Connection
    X = Add()([X, X_shortcut])
    X = Activation('relu')(X)

    return X




#Implementation of ResNet-50
def ResNet50(input_shape=(224, 224, 3)):

    X_input = Input(input_shape)

    X = ZeroPadding2D((3, 3))(X_input)

    X = Conv2D(64, (7, 7), strides=(2, 2), name='conv1', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name='bn_conv1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((3, 3), strides=(2, 2))(X)

    X = convolutional_block(X, f=3, filters=[16, 16, 64], stage=2, block='a', s=1)
    X = identity_block(X, 3, [16, 16, 64], stage=2, block='a')
    X = identity_block(X, 3, [16, 16, 64], stage=2, block='b')
    X = identity_block(X, 3, [16, 16, 64], stage=2, block='c')
    # X = identity_block(X, 3, [16, 16, 64], stage=2, block='d')


    X = convolutional_block(X, f=3, filters=[32, 32, 128], stage=3, block='b', s=2)
    X = identity_block(X, 3, [32, 32, 128], stage=3, block='a')
    X = identity_block(X, 3, [32, 32, 128], stage=3, block='b')
    # X = identity_block(X, 3, [32, 32, 128], stage=3, block='c')
    # X = identity_block(X, 3, [32, 32, 128], stage=3, block='d')

    X = convolutional_block(X, f=3, filters=[64, 64, 256], stage=4, block='c', s=2)
    X = identity_block(X, 3, [64, 64, 256], stage=4, block='a')
    # X = identity_block(X, 3, [64, 64, 256], stage=4, block='b')
    # X = identity_block(X, 3, [64, 64, 256], stage=4, block='c')
    # X = identity_block(X, 3, [64, 64, 256], stage=4, block='d')
    # X = identity_block(X, 3, [64, 64, 256], stage=4, block='e')
    # X = identity_block(X, 3, [64, 64, 256], stage=4, block='f')

    X = convolutional_block(X, f=3, filters=[128, 128, 512], stage=5, block='d', s=2)
    # X = identity_block(X, 3, [128, 128, 512], stage=5, block='a')
    # X = identity_block(X, 3, [128, 128, 512], stage=5, block='c')

    X = AveragePooling2D(pool_size=(2, 2), padding='same')(X)

    model = Model(inputs=X_input, outputs=X, name='ResNet50')

    return model


# @keras.saving.get_custom_objects().clear()

# # Creatig a proper customr ResNet50 layer for serialization
# @keras.saving.register_keras_serializable()
# class ResNet50Class(keras.layers.Layer):
    
#     def __init__(self, nested_model:Model=None):
#         super().__init__()
#         self.nested_model = nested_model
    
#     def get_config(self):
#         config = super().get_config()
#         # Updation of config with custom layer's parameters
#         for layer in self.nested_model.layers:
#             config.update(
#                 {
#                     layer.name: None
#                 }
#             )

#         return config
    
#     @classmethod
#     def from_config(cls, config):
#         return cls(**config)
    
#     def call(self, inputs):
#         return self.nested_model(inputs)
    

    
def create_model() -> Model:

    # base_model = ResNet50Class(ResNet50(input_shape=(224, 224, 3))())
    # x = base_model.nested_model.output
    base_model = ResNet50(input_shape=(224, 224, 3))
    x = base_model.output
    x = Flatten()(x)
    x = Dense(300, activation='relu', name='fc1',kernel_initializer=glorot_uniform(seed=0))(x)
    x = Dense(150, activation='relu', name='fc2',kernel_initializer=glorot_uniform(seed=0))(x)
    x = Dense(33, activation='softmax', name='fc3',kernel_initializer=glorot_uniform(seed=0))(x)

    model = Model(inputs=base_model.input, outputs=x)

    for layer in base_model.layers:
        layer.trainable = False

    return model

def save_model(model:Model):
    
    # with open("base_model.keras", "wb") as model_file:
    #     pickle.dump(model.get_weights(), model_file, protocol=pickle.HIGHEST_PROTOCOL)

    model.save("base_model.keras")

def load_weights():

    return load_model("base_model.keras")
    # with open("base_model.keras", "rb") as model_file:
    #     return pickle.load(model_file)

save_model(create_model())



    
