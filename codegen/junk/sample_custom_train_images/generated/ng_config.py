model = {
    "model_id": "1",
    "user_id": "1",
    "optimizer": "adam",
    "loss": "mean_squared_error",
    "metrics": "accuracy",
    "layers": [
        {"type": "Input", "params": {"shape": [28, 28, 1]}},
        {"type": "Flatten"},
        {"type": "Dense", "params": {"units": 10, "activation": "softmax"}},
    ],
    "input": {"type": "images"},
    "output": {"type": "float"},
}

train_data_path = "train"

use_generator_fit = True