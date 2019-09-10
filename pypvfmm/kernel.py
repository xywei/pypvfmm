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

from functools import partialmethod
import numpy as np


class KernelBase():
    def __init__(self, dtype=np.float64):
        assert dtype in [np.float32, np.float64]
        self.dtype = dtype

        if dtype == np.float32:
            self.dtype_str = 'float'
        elif dtype == np.float64:
            self.dtype_str = 'double'


class LaplaceKernel(KernelBase):
    __kernels__ = ['potential', 'gradient']


class StokesKernel(KernelBase):
    __kernels__ = ['velocity', 'pressure', 'stress', 'vel_grad']


class BiotSavartKernel(KernelBase):
    __kernels__ = ['potential']


class HelmholtzKernel(KernelBase):
    __kernels__ = ['potential']


def add_kernels(kernel_container):
    """Add kernel bindings.
    """
    def kernel(self, kernel_name):
        return "%s, %s" % (self.__class__.__name__, kernel_name)

    for kernel_name in kernel_container.__kernels__:
        named_kernel = partialmethod(kernel, kernel_name=kernel_name)
        setattr(kernel_container, kernel_name, named_kernel)


def process_sumpy_kernel(kernel):
    """Parse sumpy kernels to feed to pvfmm.
    """
    if not kernel.dim == 3:
        raise ValueError("PvFMM only supports 3D kernels.")

    from sumpy.kernel import DerivativeBase, LaplaceKernel
    if isinstance(kernel, DerivativeBase):
        if not isinstance(kernel.inner_kernel, LaplaceKernel):
            raise ValueError("PvFMM does not support computing derivatives of %s."
                             % str(kernel.inner_kernel))
        return str(kernel.inner_kernel) + ', gradient'

    return str(kernel)


add_kernels(LaplaceKernel)
add_kernels(StokesKernel)
add_kernels(BiotSavartKernel)
add_kernels(HelmholtzKernel)
