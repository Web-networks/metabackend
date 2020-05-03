import re
import sys
import logging

logger = logging.getLogger(__name__)


class JinjaRenderer(object):
    INDENT = ' '

    def __init__(self, jinja_env):
        self.jinja_env = jinja_env

    def _get_template(self, template):
        if not template.endswith('.jinja2'):
            template += '.jinja2'
        return self.jinja_env.get_template(template)

    # -> (next_indent, indent + payload)
    def _get_line_with_indent_change(self, line, prev_indent):
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
            proc_line = '\n' + next_indent * self.INDENT + payload
            return next_indent, proc_line
        else:
            return prev_indent, ' ' + payload

    def render_with_indents(self, template, **kwargs):
        if isinstance(template, str):
            logger.info('Render %s', template)
            template = self._get_template(template)
        rendered_text = template.render(**kwargs)
        indent = 0
        result = ''
        for i, line in enumerate(rendered_text.split('\n')):
            indent, proc_line = self._get_line_with_indent_change(line, indent)
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
