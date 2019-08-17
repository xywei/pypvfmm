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
from pypvfmm import cheb_utils, kernel


def test_cheb_poly_double():
    deg = 3
    npts = 100
    pts = np.linspace(0, 1, npts, dtype=np.float64)
    out = np.zeros((deg + 1) * npts, dtype=np.float64)
    cheb_utils.cheb_poly_double(deg, pts, npts, out)


def test_cheb_poly_single():
    deg = 3
    npts = 100
    pts = np.linspace(0, 1, npts, dtype=np.float32)
    out = np.zeros((deg + 1) * npts, dtype=np.float32)
    cheb_utils.cheb_poly_float(deg, pts, npts, out)


def test_integ_single():
    deg = 3
    npts = 20
    spoint = np.array([0, 0, 0], dtype=np.float32)
    sbox_r = 1.5
    lap_ker = kernel.LaplaceKernel().potential()
    uu = cheb_utils.integ_float(deg, spoint, sbox_r, npts, lap_ker)
    assert uu.dtype == np.float32


def test_integ_double():
    deg = 3
    npts = 20
    spoint = np.array([0, 0, 0], dtype=np.float64)
    sbox_r = 1.5
    lap_ker = kernel.LaplaceKernel().potential()
    uu = cheb_utils.integ_double(deg, spoint, sbox_r, npts, lap_ker)
    assert uu.dtype == np.float64
