__copyright__ = "Copyright (C) 2019 Xiaoyu Wei"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from mako.template import Template

PVFMM_HEADERS = [
        "precomp_mat.hpp"
        ]


def to_txt(lines):
    """Join lines into a single piece, with newline at
    the end of each line.
    """
    return '\n'.join(lines) + '\n'


def to_cpp(lines):
    """Join lines into a single piece, with semicolon and
    newline at the end of each line.
    """
    return ';\n'.join(lines) + ';\n'


class CXXHeaders():
    """Collection of C++ header files.
    """
    incl_template = Template("#include <${hfile}>")

    def __init__(self, hfiles):
        self.header_files = hfiles

    def __str__(self):
        return to_txt([
            self.incl_template.render(hfile=hfile)
            for hfile in self.header_files])


class TemplateClassInst():
    """Instantiation of a C++ template class.
    """
    inst_template = Template("template class ${class_id}<${template_args}>()")

    def __init__(self, class_id, template_args):
        self.class_id = class_id
        self.template_args= template_args

    def __str__(self):
        return self.inst_template.render(
            class_id=self.class_id,
            template_args=', '.join(self.template_args),
            )


# TODO: find instantiations from src/ and generate wrappers.

# TODO: instantiate internal template stuff and generate wrappers.
# (e.g. PrecompMat<Real_t>)
