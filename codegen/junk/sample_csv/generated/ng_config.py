model = {
    "model_id": "1",
    "user_id": "1",
    "optimizer": "adam",
    "loss": "sparse_categorical_crossentropy",
    "metrics": "accuracy",
    "layers": [{"type": "Dense", "params": {"units": 1}}],
    "input": {"type": "csv", "target": "survived"},
    "output": {"type": "float"},
}

train_data_path = "train"

use_generator_fit = False

input_shape = (10,)
