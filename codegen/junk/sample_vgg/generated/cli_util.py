import pathlib
import json
import logging
import os


def do_eval(args, io, train):

    if os.path.isdir(args.eval_data):
        base_dir = pathlib.Path(args.eval_data)
        filenames = os.listdir(base_dir)
        filenames = list(filter(lambda x: not x.endswith(".csv"), filenames))
        filepaths = list(map(lambda x: base_dir / x, filenames))
    else:
        filenames = [args.eval_data]
        filepaths = filenames

    logging.debug("eval files: %s", filenames)
    X = io.read_eval_data(filepaths)
    result = train.do_eval(X)
    eval_result = json.dumps(
        {"eval_result": {filename: out for filename, out in zip(filenames, result)}}
    )
    logging.info("eval result: %s", eval_result)
    open(args.network_output, "w").write(eval_result)
