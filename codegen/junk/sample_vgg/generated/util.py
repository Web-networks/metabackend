from tensorflow import keras
import tensorflow as tf
import numpy as np
import pathlib
import sklearn
from sklearn.model_selection import train_test_split

import ng_config


def load_images(filenames):
    X = np.array(
        [
            tf.io.decode_image(
                open(filename, "rb").read(),
                channels=ng_config.model["input"]["channels"],
            ).numpy()
            for filename in filenames
        ]
    )

    X = tf.image.resize(X, ng_config.model["input"]["dimensions"]).numpy()

    return X


def read_train_val_images(basedir, rescale=1 / 255):
    # here not to break missing deps where unneeded
    import pandas

    basedir = pathlib.Path(basedir)
    df = pandas.read_csv(basedir / "dataset.csv")
    filenames = list(df["filename"])
    outputs = list(df["output"])

    X_train = load_images(map(lambda filename: basedir / filename, filenames))

    if ng_config.model["output"]["type"] == "float":
        y_train = [float(y) for y in outputs]
    else:
        y_train = outputs

    y_train = np.array(y_train)

    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.33, random_state=42
    )

    return (X_train, y_train), (X_val, y_val)


def read_csv(filename):
    import pandas

    df = pandas.read_csv(filename)
    print(df.head())
