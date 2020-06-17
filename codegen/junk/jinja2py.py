import re
import sys

import jinja2
from jinja2.loaders import FileSystemLoader

from config import TEMPLATES_PATH

jenv = jinja2.Environment(loader=FileSystemLoader(TEMPLATES_PATH),
                          trim_blocks=True, 
                          lstrip_blocks=True,
                          extensions=['jinja2.ext.do'])

def get_template(name):
  return jenv.get_template(name)


INDENT = ' '

# -> (next_indent, indent + payload)
def _get_line_with_indent_change(line, prev_indent):
  regexp = r'^([\s<>|]*)(.*)$'
  indent_markers, payload = re.match(regexp, line).groups()

  next_indent: int = None

  if indent_markers.count('<'):
    next_indent = prev_indent + 1
  elif indent_markers.count('>'):
    next_indent = prev_indent - 1
  elif indent_markers.count('|'):
    next_indent = prev_indent

  if next_indent is not None:
    proc_line = '\n' + next_indent * INDENT + payload
    return next_indent, proc_line
  else:
    return prev_indent, ' ' + payload


def render_with_indents(template, **kwargs):
  filename = None
  if isinstance(template, str):
    filename = template
    template = get_template(template)
  rendered_text = template.render(**kwargs)
  indent = 0
  result = ''
  for i, line in enumerate(rendered_text.split('\n')):
    indent, proc_line = _get_line_with_indent_change(line, indent)
    if indent < 0:
      print('Error preparing rendered text:', file=sys.stderr)
      print(rendered_text, file=sys.stderr)
      print('At line', i + 1, file=sys.stderr)
      assert False
    result += proc_line
  if indent != 0:
    print('Error preparing rendered text:', file=sys.stderr)
    print(rendered_text, file=sys.stderr)
    print('At (last) line', i + 1, file=sys.stderr)
    assert False
  return result
