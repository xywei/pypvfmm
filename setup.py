#!/usr/bin/env python

"""Setup script.
"""

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

import subprocess
import os

PYPVFMM_SRC_DIR = os.getcwd()


# {{{ setup package version


def get_version():
    ver_dic = {}
    version_file = open("pypvfmm/version.py")
    try:
        version_file_contents = version_file.read()
    finally:
        version_file.close()

    exec(compile(version_file_contents, "pypvfmm/version.py", 'exec'), ver_dic)

    return ver_dic

# }}} End setup package version


# {{{ setup bundled pvfmm

def build_pvfmm():
    """Build the bundled pvfmm.
    """
    # if is in git dir, update submodules
    if os.path.exists(os.path.join(PYPVFMM_SRC_DIR, '.git')):
        print("Updating submodules")
        subprocess.call(["git", "submodule", "update",
                         "--init", "--recursive"])

    print("Entering pvfmm/")
    os.chdir(os.path.join(PYPVFMM_SRC_DIR, 'pvfmm'))

    subprocess.call(["libtoolize"])
    subprocess.call(["aclocal"])
    subprocess.call(["autoconf"])
    subprocess.call(["autoheader"])
    subprocess.call(["automake", "--add-missing"])

    subprocess.call(["./configure",
                     "--prefix=%s/pvfmm-build" % PYPVFMM_SRC_DIR])
    subprocess.call(["make", "-j%d" % os.cpu_count()])
    subprocess.call(["make", "install"])

    print("Leaving pvfmm/")
    os.chdir(PYPVFMM_SRC_DIR)

# }}} End setup bundled pvfmm


def main():
    """By default a bundled version of pvfmm is built, which requires
    autotools. User can also specify to build against an existing pvfmm
    installation by setting the PVFMM_DIR environment variable to point
    to the path containing the MakeVariables file.
    """

    external_pvfmm = os.environ.get("PVFMM_DIR", None)

    if external_pvfmm:
        use_bundled_pvfmm = False
        pvfmm_dir = external_pvfmm
        print("Using external PVFMM installed at %s." % external_pvfmm)
    else:
        use_bundled_pvfmm = True
        pvfmm_dir = os.path.join(PYPVFMM_SRC_DIR,
                                 "pvfmm-build", "share", "pvfmm")
        print("Building with bundled PVFMM")

    if use_bundled_pvfmm:
        build_pvfmm()

    if not os.path.isfile(os.path.join(pvfmm_dir, "MakeVariables")):
        raise FileNotFoundError("Cannot locate MakeVariables at %s. "
                                "Please check whether PVFMM_DIR "
                                "is set up correctly." % pvfmm_dir)

    from distutils.core import setup

    ver_dic = get_version()

    setup(name="pypvfmm",
          version=ver_dic["VERSION_TEXT"],
          description="Python wrappers for Dhairya Malhotra's pvfmm library",
          long_description=open("README.rst", "rt").read(),
          author="Xiaoyu Wei",
          author_email="xywei@pm.me",
          license="wrapper: MIT/pvfmm: LGPLv3/pybind11: 3-clause BSD",
          url="http://github.com/xywei/pypvfmm",
          classifiers=[
              'Development Status :: 2 - Pre-Alpha',
              'Intended Audience :: Developers',
              'Intended Audience :: Other Audience',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: MIT License',
              'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',  # noqa: E501
              'License :: OSI Approved :: BSD License',
              'Programming Language :: C++',
              'Programming Language :: Python',
              'Topic :: Scientific/Engineering',
              'Topic :: Scientific/Engineering :: Mathematics',
              'Topic :: Software Development :: Libraries',
              ],

          packages=["pypvfmm"],
          )


if __name__ == '__main__':
    main()
