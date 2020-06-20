import argparse
import json
import sys
import os

import black

import jinja2py
from config import TEMPLATES_PATH


def render_template(model, template_name):
    input_template = template_name + '.py.jinja2'
    code = jinja2py.render_with_indents(
        input_template, model=model, str=str, repr=repr,
        layer_types=set(map(lambda x: x['type'], model['layers'])),
    )
    return code


def format_and_write(template_name, code, output_dir):
    try:
        code = black.format_str(code, mode=black.FileMode())
    except:
        print('black had error formatting code:', file=sys.stderr)
        print(code, file=sys.stderr)
        raise
    with open(output_dir + template_name + '.py', 'w') as f:
        f.write(code)

parser = argparse.ArgumentParser()
parser.add_argument('--case')
args = parser.parse_args()

case = args.case

model = json.load(open(f'{case}/model.json'))

for module in ['model', 'ng_input', 'train', 'ng_bus', 'cli', 'ng_config', 'util']:
    naive_path = f'{TEMPLATES_PATH}/{module}.py'
    if os.path.exists(naive_path):
        code = open(naive_path).read()
    else:
        code = render_template(model, module)
    format_and_write(module, code, f'{case}/generated/')
