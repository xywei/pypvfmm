from __future__ import division, absolute_import, print_function

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
from codegen_helpers import CXXClass, CXXFunction

PVFMM_HEADERS = ["pvfmm.hpp", ]
PYBIND11_HEADERS = ["pybind11/pybind11.h", "pybind11/numpy.h"]

PVFMM_SUBMODULES = ["kernel", "precomp_mat", "cheb_utils"]

# the list ordering matters
PVFMM_NUMPY_WRAPPERS = ["kernel", "cheb_utils"]

PVFMM_CLASSES = []
PVFMM_FUNCTIONS = []


def register_class(cxxclass):
    global PVFMM_CLASSES
    PVFMM_CLASSES.append(cxxclass)


def register_function(cxxfunc):
    global PVFMM_FUNCTIONS
    PVFMM_FUNCTIONS.append(cxxfunc)


# {{{ mod: precomp_mat

class_precomp_mat = CXXClass(class_name="PrecompMat",
                             template_args=["double", ],
                             type_str="D",
                             in_module="precomp_mat")

class_precomp_mat.add_member_func(is_constructor=True,
                                  docstring="Constructor.",
                                  arg_names=["scale_invar"],
                                  arg_types=["bool"],
                                  )

register_class(class_precomp_mat)

# }}} End mod: precomp_mat

# {{{ mod: cheb_utils

# cheb_poly
cheb_poly_doc = '\\n'.join([
    "Returns the values of all chebyshev polynomials up to degree d,",
    "evaluated at points in the input vector. Output format:",
    "{ T0[in[0]], ..., T0[in[n-1]], T1[in[0]], ..., T(d-1)[in[n-1]] }",
    ])


def wrap_cheb_poly(number_type):
    func_cheb_poly = CXXFunction(function_name='cheb_poly',
                                 in_module='cheb_utils',
                                 namespace_prefix='pypvfmm::',
                                 docstring=cheb_poly_doc,
                                 template_args=["%s" % number_type, ],
                                 type_str='_%s' % number_type,
                                 arg_names=['d', 'in', 'n', 'out'],
                                 )
    register_function(func_cheb_poly)


wrap_cheb_poly('double')
wrap_cheb_poly('float')


# integ
integ_doc = """Compute integrals over pyramids in all directions.

:param m: int, Chebyshev degree
:param s: numpy.array, singular (target) point
:param r: float, box size
:param n: int, degree of the quadrature rule
:param kernel: str, kernel information, see :mod:`pypvfmm.kernel`

:return: numpy.array, the computed integrals
""".replace('\n', '\\n')


def wrap_integ(number_type):
    func_cheb_poly = CXXFunction(function_name='integ',
                                 in_module='cheb_utils',
                                 namespace_prefix='pypvfmm::',
                                 docstring=integ_doc,
                                 template_args=["%s" % number_type, ],
                                 type_str='_%s' % number_type,
                                 arg_names=['m', 's', 'r', 'n', 'kernel'],
                                 )
    register_function(func_cheb_poly)


wrap_integ('double')
wrap_integ('float')

# }}} End mod: cheb_utils
