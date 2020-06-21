model = {
    "model_id": "vgg",
    "user_id": "1",
    "optimizer": "adam",
    "loss": "sparse_categorical_crossentropy",
    "metrics": "accuracy",
    "layers": [
        {
            "type": "Conv2D",
            "params": {
                "input_shape": [32, 32, 3],
                "filters": 64,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 64,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {"type": "MaxPool2D", "params": {"pool_size": [2, 2], "strides": [2, 2]}},
        {
            "type": "Conv2D",
            "params": {
                "filters": 128,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 128,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {"type": "MaxPool2D", "params": {"pool_size": [2, 2], "strides": [2, 2]}},
        {
            "type": "Conv2D",
            "params": {
                "filters": 256,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 256,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 256,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {"type": "MaxPool2D", "params": {"pool_size": [2, 2], "strides": [2, 2]}},
        {
            "type": "Conv2D",
            "params": {
                "filters": 512,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 512,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 512,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {"type": "MaxPool2D", "params": {"pool_size": [2, 2], "strides": [2, 2]}},
        {
            "type": "Conv2D",
            "params": {
                "filters": 512,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 512,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {
            "type": "Conv2D",
            "params": {
                "filters": 512,
                "kernel_size": [3, 3],
                "padding": "same",
                "activation": "relu",
            },
        },
        {"type": "Flatten", "params": {}},
        {"type": "Dense", "params": {"units": 4096, "activation": "relu"}},
        {"type": "Dense", "params": {"units": 4096, "activation": "relu"}},
        {"type": "Dense", "params": {"units": 10, "activation": "softmax"}},
    ],
    "input": {
        "type": "builtin_dataset",
        "dataset": "cifar100",
        "dimensions": [32, 32],
        "channels": 3,
    },
    "output": {"type": "integer", "range": [0, 10]},
}

train_data_path = "train"

use_generator_fit = False

input_shape = (32, 32, 3)
