pypvfmm: A Python Wrapper of PVFMM
==================================

.. image:: https://gitlab.tiker.net/xywei/pypvfmm/badges/master/pipeline.svg
   :target: https://gitlab.tiker.net/xywei/pypvfmm/commits/master

pypvfmm is a **WIP** (not-yet-functional) Python interface to pvfmm. 

Current Status
--------------

The wrapper was initially developed to support precomputation tests in `volumential`.
At the moment, only the table builder is wrapped. Additional functionalities will
be added as needed. The existing build system and `setuptools` integration
allows for relatively easy addition of new functionalities.

Conda
-----

To use `pypvfmm` inside a `conda` environment, install the following dependencies
from `conda-forge`:

- `c-compiler`, `cxx-compiler`, `fortran-compiler`, and `libcxx`.
- `xorg-libx11`
- `mako`
- `numpy` (which also installs `BLAS` as its dependency).
- `pybind11`
- `openmp`
- `mpi4py` (which also installs `mpich` as its dependency).
- `fftw`

.. code-block:: sh

  conda install -c conda-forge c-compiler cxx-compiler fortran-compiler libcxx xorg-libx11 mako numpy pybind11 openmp mpi4py fftw
  conda install -c conda-forge pytest pudb

License
-------

`pvfmm` is licensed under the LGPL-3.0 license.

This wrapper is licensed under the MIT license, as below.

Copyright (C) 2019 Xiaoyu Wei

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
