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

import numpy as np
from pypvfmm.wrapper.cheb_utils import integ_double, integ_float
from pypvfmm.wrapper.cheb_utils import cheb_poly_float, cheb_poly_double


def cheb_poly(d, vec_in, n, vec_out):
    assert isinstance(vec_in, np.ndarray)
    assert isinstance(vec_out, np.ndarray)
    assert vec_in.dtype == vec_out.dtype
    dtype = vec_in.dtype

    if dtype == np.float32:
        return cheb_poly_float(d, vec_in, n, vec_out)
    elif dtype == np.float64:
        return cheb_poly_double(d, vec_in, n, vec_out)


def integ(m, s, r, n, kernel):
    """Compute integrals over pyramids in all directions.
    The source region is [0, r]^3.

    :param m: int, Chebyshev degree
    :param s: numpy.array, singular (target) point
    :param r: float, box size
    :param n: int, degree of the quadrature rule
    :param kernel: str, kernel information, see :mod:`pypvfmm.kernel`

    :return: numpy.array, the computed integrals
    """
    assert isinstance(s, np.ndarray)
    assert len(s) == 3

    dtype = s.dtype

    if dtype == np.float32:
        return integ_float(m, s, r, n, kernel)
    elif dtype == np.float64:
        return integ_double(m, s, r, n, kernel)

    raise NotImplementedError("No fallback wrapper for dtype %s." % str(dtype))
