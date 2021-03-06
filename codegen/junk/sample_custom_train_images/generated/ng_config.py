model = {
    "model_id": "1",
    "user_id": "1",
    "optimizer": "adam",
    "loss": "mean_squared_error",
    "metrics": "accuracy",
    "layers": [{"type": "Flatten"}, {"type": "Dense", "params": {"units": 1}}],
    "input": {"type": "images", "dimensions": [28, 28], "channels": 1},
    "output": {"type": "float"},
}

train_data_path = "train"

use_generator_fit = True

input_shape = (28, 28, 1)
