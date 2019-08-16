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


class CXXFunction():
    """C++ function.
    """
    func_template = Template(
        '${mod_var}.def("${function_name}${type_str}", '
        '&${namespace_prefix}${function_name}${template_args}'
        '${docstring}${kwargs}${return_policy});')

    def __init__(self, function_name, namespace_prefix="pvfmm::",
                 in_module='m', return_policy=None,
                 docstring=None,
                 template_args=None, type_str="_unknown",
                 arg_names=None, arg_default_vals=None,):
        self.function_name = function_name
        self.namespace_prefix = namespace_prefix

        if in_module == 'm':
            self.in_module = in_module
        else:
            self.in_module = 'mod_' + in_module

        if return_policy:
            assert return_policy in [
                'take_ownership', 'copy', 'move', 'reference',
                'reference_internal', 'automatic', 'automatic_reference']
            self.return_policy = (
                ', pybind11::return_value_policy::' + return_policy)
        else:
            self.return_policy = ''

        if template_args is None:
            self.template_args = []
        else:
            self.template_args = template_args

        if docstring is None:
            self.docstring = ''
        else:
            self.docstring = ', "%s"' % docstring

        if len(self.template_args) > 0:
            self.type_str = type_str
        else:
            self.type_str = ""

        if arg_names is None:
            self.arg_names = []
        else:
            self.arg_names = arg_names

        if arg_default_vals is None:
            self.arg_default_vals = dict()
        else:
            self.arg_default_vals = arg_default_vals

    def generate_template_args_code(self):
        """Example output: <cdouble>
        """
        if len(self.template_args) < 1:
            return ''
        args_code = ', '.join(self.template_args)
        return '<%s>' % args_code

    def generate_kwargs_code(self):
        """Example output: pybind11::arg("n") = 3
        """
        if len(self.arg_names) < 1:
            return ''
        code_segs = []
        for arg in self.arg_names:
            seg = 'pybind11::arg("%s")' % arg
            if arg in self.arg_default_vals:
                seg = seg + (' = %s' % self.arg_default_vals[arg])
            code_segs.append(seg)
        return ', ' + ', '.join(code_segs)

    def __str__(self):
        context = {
            "mod_var": self.in_module,
            "namespace_prefix": self.namespace_prefix,
            "function_name": self.function_name,
            "template_args": self.generate_template_args_code(),
            "type_str": self.type_str,
            "docstring": self.docstring,
            "kwargs": self.generate_kwargs_code(),
            "return_policy": self.return_policy,
            }

        return self.func_template.render(**context)


class TemplateClassInst():
    """Instantiation of a C++ template class.

    tplt_class_id: class identifier (without template args), e.g. std::vector.
    """
    inst_template = Template("template class ${tplt_class_id}<${template_args}>")

    class_id_template = Template("${tplt_class_id}<${template_args}>")

    def __init__(self, tplt_class_id, template_args, namespace_prefix='pvfmm::'):
        self.tplt_class_id = tplt_class_id
        self.template_args = template_args
        self.namespace_prefix = namespace_prefix

    def __str__(self):
        return self.inst_template.render(
            tplt_class_id=self.namespace_prefix + self.tplt_class_id,
            template_args=', '.join(self.template_args),
            )

    def get_class_id(self):
        """Returns class id that can be used to construct CXXClass objects.
        """
        return self.class_id_template.render(
            tplt_class_id=self.namespace_prefix + self.tplt_class_id,
            template_args=', '.join(self.template_args),
            )


class CXXClassMemberBase():
    """C++ class members.
    """


class CXXClassMemberFunc(CXXClassMemberBase):
    """Member function of a C++ class.
    """
    normal_template = Template(
        '.def("${name}", &${class_id}::${name}, "${docstring}", ${kwargs})')

    static_template = Template(
        '.def_static("${name}", &${class_id}::${name}, "${docstring}", ${kwargs})')

    constructor_template = Template(
        '.def(pybind11::init<${arg_types}>(), "${docstring}", ${kwargs})')

    def __init__(self, name=None, arg_names=None, arg_types=None,
                 arg_default_vals=None,
                 docstring=None, is_static=False, is_constructor=False):
        if name is None:
            assert is_constructor
            self.name = ""
        else:
            self.name = name

        if arg_names:
            self.arg_names = arg_names
        else:
            self.arg_names = []

        if arg_types:
            self.arg_types = arg_types
        else:
            self.arg_types = []

        if arg_default_vals:
            self.arg_default_vals = arg_default_vals
        else:
            self.arg_default_vals = dict()

        if docstring:
            self.docstring = docstring
        else:
            self.docstring = ""

        self.is_static = is_static
        self.is_constructor = is_constructor

        # static constructor should not be a thing
        assert not (is_constructor and is_static)

    def generate_kwargs_code(self):
        """Example output: pybind11::arg("n") = 3
        """
        code_segs = []
        for arg in self.arg_names:
            seg = 'pybind11::arg("%s")' % arg
            if arg in self.arg_default_vals:
                seg = seg + (' = %s' % self.arg_default_vals[arg])
            code_segs.append(seg)
        return ', '.join(code_segs)

    def __str__(self):
        context = {
            "name": self.name,
            "docstring": self.docstring,
            "kwargs": self.generate_kwargs_code(),
            "arg_types": ", ".join(self.arg_types),
            }
        if self.is_static:
            return self.static_template.render(**context)
        if self.is_constructor:
            return self.constructor_template.render(**context)

        return self.normal_template.render(**context)


class CXXClass():
    """C++ class.
    """
    class_template = Template(
        'pybind11::class_<${class_id}>(${mod_var}, "${class_name}"${dynamic_flag})${members};')  # noqa: E501

    def __init__(self, class_name, namespace_prefix="pvfmm::",
                 in_module='m', class_members=None,
                 template_args=None, type_str="Unknown",
                 is_dynamic=True):
        self.class_name = class_name
        self.is_dynamic = is_dynamic
        self.type_str = type_str

        if in_module == 'm':
            self.in_module = in_module
        else:
            self.in_module = 'mod_' + in_module

        if template_args is None:
            self.template_args = []
        else:
            self.template_args = template_args

        self.class_instantiation = TemplateClassInst(
            self.class_name, self.template_args)

        if class_members is None:
            self.class_members = []
        else:
            assert isinstance(class_members, list)
            for member in class_members:
                assert isinstance(member, CXXClassMemberBase)
            self.class_members = class_members

    def add_member_func(self, *args, **kwargs):
        """Add a member function to the class.
        """
        self.class_members.append(CXXClassMemberFunc(*args, **kwargs))

    def __str__(self):

        if self.is_dynamic:
            dynamic_flag = ', pybind11::dynamic_attr()'
        else:
            dynamic_flag = ''

        context = {
            "class_id": self.class_instantiation.get_class_id(),
            "class_name": self.class_name + self.type_str,
            "dynamic_flag": dynamic_flag,
            "mod_var": self.in_module,
            "members": '\n    ' + '\n    '.join(
                [Template(str(member)).render(
                    class_id=self.class_instantiation.get_class_id())
                 for member in self.class_members]),
            }

        return self.class_template.render(**context)


# TODO: find instantiations from src/ and generate wrappers.

# TODO: instantiate internal template stuff and generate wrappers.
# (e.g. PrecompMat<Real_t>)
