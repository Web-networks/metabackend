from django.apps import AppConfig

import os

import jinja2
from jinja2 import loaders

import codegen.jinja2py as jinja2py

TEMPALTES_PATH = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_RENDERER = jinja2py.JinjaRenderer(None)

BANED_NAMES = (
    'neurogen_parsers.py.jinja2',
)
GENERATE_NAMES = list()
CODES = dict()


class CodegenConfig(AppConfig):
    name = 'codegen'

    def ready(self):
        global JINJA_RENDERER
        jinja_env = jinja2.Environment(
            loader=loaders.FileSystemLoader(TEMPALTES_PATH),
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=['jinja2.ext.do']
        )
        JINJA_RENDERER = jinja2py.JinjaRenderer(jinja_env)

        generate_names = list()
        codes = dict()
        for f in os.listdir(TEMPALTES_PATH):
            if f in BANED_NAMES:
                continue
            if os.path.isfile(os.path.join(TEMPALTES_PATH, f)):
                if f.endswith('.py.jinja2'):
                    generate_names.append(f[:-len('.jinja2')])
                elif f.endswith('.py'):
                    with open(os.path.join(TEMPALTES_PATH, f)) as c:
                        codes[f] = c.read()

        global GENERATE_NAMES
        GENERATE_NAMES = generate_names
        global CODES
        CODES = codes
