model = {
    "model_id": "1",
    "user_id": "1",
    "optimizer": "adam",
    "loss": "binary_crossentropy",
    "metrics": "accuracy",
    "layers": [
        {"type": "Dense", "params": {"units": 2, "activation": "relu"}},
        {"type": "Dense", "params": {"units": 1, "activation": "relu"}},
    ],
    "input": {
        "type": "csv",
        "features": [
            {"name": "sex", "type": "enum", "enum": ["male", "female"]},
            {"name": "class", "type": "enum", "enum": ["First", "Second", "Third"]},
            {"name": "alone", "type": "enum", "enum": ["n", "y"]},
            {"name": "n_siblings_spouses", "type": "float"},
            {"name": "parch", "type": "float"},
        ],
        "target": {"name": "survived", "type": "integer"},
    },
    "output": {"type": "bool", "target": "csv", "name": "survived_out"},
}

train_data_path = "train"

use_generator_fit = False

input_shape = (5,)
