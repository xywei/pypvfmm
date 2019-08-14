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
from codegen_helpers import TemplateClassInst, CXXClass

PVFMM_HEADERS = ["pvfmm.hpp", ]
PYBIND11_HEADERS = ["pybind11/pybind11.h", "pybind11/numpy.h"]

PVFMM_SUBMODULES = ["precomp_mat", "profile"]

# Try out on one class
class_precomp_mat_pre = TemplateClassInst("PrecompMat", ["double", ])
class_precomp_mat = CXXClass(class_precomp_mat_pre.get_class_id(),
                             class_precomp_mat_pre.tplt_class_id + 'D',
                             in_module="precomp_mat")
class_precomp_mat.add_member_func(is_constructor=True,
                                  docstring="Constructor.",
                                  arg_names=["scale_invar"],
                                  arg_types=["bool"],
                                  arg_default_vals={"scale_invar": True}
                                  )

print(class_precomp_mat)
