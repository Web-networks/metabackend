import argparse
import os
import random
import logging
import json

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

# eval options
parser.add_argument('--eval-data')
parser.add_argument('--network-output')

args = parser.parse_args()

logging.debug('args: %s', args)

bus = ng_bus.NeurogenBus(args.mode)
io = ng_input.NeurogenIO(bus)
train = train.TrainController()

if args.mode == 'train':
    train_data, val_data = io.read_train_data(args.sample_count)

    if not ng_config.use_generator_fit:
        logging.info('X_train shape: %s', train_data[0].shape)

train.do_compile()
train.try_load_weights(args.weights)

if args.mode == 'train':
    train.print_sample_predictions(*val_data)
    result_of_train = train.do_train(
        train_data, val_data,
        args.epochs, args.weights,
    )
    logging.info('history: %s', result_of_train.history)
    # print(np.mean(result_of_train.history["val_acc"]))
    train.print_sample_predictions(*val_data)
elif args.mode == 'eval':
    assert args.eval_data
    assert args.network_output
    logging.debug('eval content: %s', os.listdir(args.eval_data))
    eval_result = json.dumps({
        'eval_result': {
            filename: random.randint(0, 9)
            for filename in os.listdir(args.eval_data)
        }
    })
    logging.info('eval result: %s', eval_result)
    open(args.network_output, 'w').write(eval_result)

from tensorflow.keras import backend as K

K.clear_session()
