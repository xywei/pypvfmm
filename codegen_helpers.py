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

    tplt_class_id: class identifier (without template args), e.g. std::vector.
    """
    inst_template = Template("template class ${tplt_class_id}<${template_args}>")

    class_id_template = Template("${tplt_class_id}<${template_args}>")

    def __init__(self, tplt_class_id, template_args):
        self.tplt_class_id = tplt_class_id
        self.template_args = template_args

    def __str__(self):
        return self.inst_template.render(
            tplt_class_id=self.tplt_class_id,
            template_args=', '.join(self.template_args),
            )

    def get_class_id(self):
        """Returns class id that can be used to construct CXXClass objects.
        """
        return self.class_id_template.render(
            tplt_class_id=self.tplt_class_id,
            template_args=', '.join(self.template_args),
            )


class CXXClass():
    """C++ Class.

    class_id: class identifier (w/t template arguments), e.g. std::vector<double>.
    class_name: Python class name, e.g. StdVector.
    mod_var: variable for module construction in pybind11.
    member_name: name of class member functions.
    """
    class_template = Template(
        'pybind11::class_<${class_id}>(${mod_var}, "${class_name}")${members};')

    member_template = Template(
        '\n.def("${member_name}", &${class_id}::${member_name}, '
        '"${member_docstring}", ${func_arg_names}')

    arg_name_template = Template(
        'pybind11::arg("${arg_name}")')

    def __init__(self, class_id, class_name,
                 member_func_names, member_docs, member_arg_names,
                 mod_var='m'):
        self.class_id = class_id
        self.class_name = class_name
        self.mod_var = mod_var

        assert isinstance(member_func_names, list)
        for mfunc in member_func_names:
            assert isinstance(mfunc, str)
        self.member_func_names = member_func_names

        assert isinstance(member_docs, dict)
        self.member_docs = member_docs
        assert isinstance(member_arg_names, dict)
        self.member_arg_names = member_arg_names

# TODO: find instantiations from src/ and generate wrappers.

# TODO: instantiate internal template stuff and generate wrappers.
# (e.g. PrecompMat<Real_t>)
