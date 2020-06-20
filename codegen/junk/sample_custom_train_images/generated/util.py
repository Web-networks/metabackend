import keras

import ng_config


def read_train_val_images(dirname, target_size, rescale=1 / 255):
    gen = keras.preprocessing.image.ImageDataGenerator(
        rescale=rescale, shear_range=0.2, zoom_range=0.2, horizontal_flip=True,
    )
    train_gen = gen.flow_from_directory(
        dirname,
        target_size=target_size,
        color_mode="grayscale",
        batch_size=32,
        classes=list(map(str, range(0, 10))),
        shuffle=True,
        seed=42,
        # subset='training',
    )
    # val_gen = gen.flow_from_directory(
    #     dirname,
    #     target_size=target_size,
    #     color_mode='grayscale',
    #     batch_size=batch_size,
    #     classes=list(range(0, 10)),
    #     shuffle=True,
    #     seed=42,
    #     subset='validation',
    # )
    val_gen = None
    return train_gen, val_gen
