import argparse
import os
import random
import logging
import json
import pathlib

import ng_bus
import ng_config
import ng_input
import train

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.DEBUG)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
root_logger.addHandler(log_handler)

parser = argparse.ArgumentParser()

# common options
parser.add_argument('--mode', required=True, choices=['train', 'eval'])

# train options
parser.add_argument('--epochs', default=5, type=int)
parser.add_argument('--sample-count', type=int)
parser.add_argument('--weights', default='weights.h5')
parser.add_argument('--metrics-output')
parser.add_argument('--train-data-dir')

# eval options
parser.add_argument('--eval-data')
parser.add_argument('--network-output')

args = parser.parse_args()

logging.debug('args: %s', args)

bus = ng_bus.NeurogenBus(args.mode)
io = ng_input.NeurogenIO(bus)
train = train.TrainController()

if args.train_data_dir:
    ng_config.train_data_path = args.train_data_dir

if args.mode == 'train':
    train_data, val_data = io.read_train_data(args.sample_count)

    if not ng_config.use_generator_fit:
        logging.info('X_train shape: %s', train_data[0].shape)
    
    logging.info('y_train shape: %s', train_data[1].shape)

train.do_compile()
train.try_load_weights(args.weights)

if args.mode == 'train':
    train.print_sample_predictions(val_data)
    result_of_train = train.do_train(
        train_data, val_data,
        args.epochs, args.weights,
    )
    metrics_output = json.dumps({
        'history': result_of_train.history
    })
    logging.info('history: %s', metrics_output)
    if args.metrics_output:
        open(args.metrics_output, 'w').write(metrics_output)
    # print(np.mean(result_of_train.history["val_acc"]))
    train.print_sample_predictions(val_data)
elif args.mode == 'eval':
    assert args.eval_data
    assert args.network_output
    import cli_util
    cli_util.do_eval(args, io, train)

from tensorflow.keras import backend as K

K.clear_session()
