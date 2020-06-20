import copy
import black
import tarfile
from io import BytesIO

import codegen.apps as codegen


def generate_code(model):
    code = copy.deepcopy(codegen.CODES)
    for name in codegen.GENERATE_NAMES:
        rendered_code = codegen.JINJA_RENDERER.render_with_indents(
            name,
            model=model, str=str, repr=repr,
            layer_types=sorted(set(map(lambda x: x['type'], model['layers']))),
        )
        formatted_code = black.format_str(rendered_code, mode=black.FileMode())
        code[name] = formatted_code
    return code


def generate_tar_archive(model):
    code = generate_code(model)
    file_out = BytesIO()
    with tarfile.open(fileobj=file_out, mode='w:gz') as tar:
        for file_name, file_content in code.items():
            tarinfo = tarfile.TarInfo(name=file_name)
            file_content = file_content.encode()
            tarinfo.size = len(file_content)
            file_content = BytesIO(file_content)
            tar.addfile(tarinfo, fileobj=file_content)
    return file_out.getvalue()
