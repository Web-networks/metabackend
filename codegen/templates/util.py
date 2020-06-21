from tensorflow import keras
import tensorflow as tf
import numpy as np
import pathlib
import sklearn
from sklearn.model_selection import train_test_split

import ng_config

def read_train_val_images(basedir, rescale=1/255):
    # here not to break missing deps where unneeded
    import pandas

    basedir = pathlib.Path(basedir)
    df = pandas.read_csv(basedir / 'dataset.csv')
    filenames = list(df['filename'])
    outputs = list(df['output'])

    print(filenames)
    print(outputs)

    X_train = np.array([
        tf.io.decode_image(
            open(basedir / filename, 'rb').read(), 
            channels=ng_config.model['input']['channels']
        ).numpy()
        for filename in filenames
    ])

    X_train = tf.image.resize(X_train, ng_config.model['input']['dimensions']).numpy()

    if ng_config.model['output']['type'] == 'float':
        y_train = [float(y) for y in outputs]
    else:
        y_train = outputs

    y_train = np.array(y_train)

    X_train, X_val, y_train, y_val = \
        train_test_split(
            X_train, y_train,
            test_size=0.33, random_state=42
        )
    
    print(X_train.shape)
    print(y_train.shape)

    return (X_train, y_train), (X_val, y_val)
