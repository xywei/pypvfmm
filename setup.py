#!/usr/bin/env python

"""Setup script.
   Partially based on https://github.com/pybind/python_example.
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
import sys
import re
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import setuptools

PYPVFMM_SRC_DIR = os.getcwd()
EXTERNAL_PVFMM = os.environ.get("PVFMM_DIR", None)


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
    # skip if the install dir exists
    if os.path.exists(os.path.join(PYPVFMM_SRC_DIR, 'pvfmm-build')):
        print("Skipping due to existing builds.")
        print("  (To rebuild, remove pvfmm-build/ and re-run the script.)")
        return

    # if is in git dir, update submodules
    if os.path.exists(os.path.join(PYPVFMM_SRC_DIR, '.git')):
        print("Updating submodules")
        subprocess.check_call(["git", "submodule", "update",
                               "--init", "--recursive"])

    print("Entering pvfmm/")
    os.chdir(os.path.join(PYPVFMM_SRC_DIR, 'pvfmm'))

    if os.path.isfile(os.path.join(os.getcwd(), 'Makefile')):
        print("Using existing Makefile for PVFMM")
    else:
        subprocess.check_call(["libtoolize"])
        subprocess.check_call(["aclocal"])
        subprocess.check_call(["autoconf"])
        subprocess.check_call(["autoheader"])
        subprocess.check_call(["automake", "--add-missing"])

        subprocess.check_call(["CXXFLAGS=-fPIC ./configure",
                               "--prefix=%s/pvfmm-build" % PYPVFMM_SRC_DIR,
                               "--disable-doxygen-dot"])

    subprocess.check_call(["make", "-j%d" % os.cpu_count()])
    subprocess.check_call(["make", "install"])

    print("Leaving pvfmm/")
    os.chdir(PYPVFMM_SRC_DIR)


if EXTERNAL_PVFMM:
    USE_BUNDLED_PVFMM = False
    PVFMM_DIR = EXTERNAL_PVFMM
    print("Using external PVFMM installed at %s." % EXTERNAL_PVFMM)
else:
    USE_BUNDLED_PVFMM = True
    PVFMM_DIR = os.path.join(PYPVFMM_SRC_DIR,
                             "pvfmm-build", "share", "pvfmm")
    print("Building with bundled PVFMM")

if USE_BUNDLED_PVFMM:
    build_pvfmm()

# }}} End setup bundled pvfmm


# {{{ setup pvfmm include and linker flags

if not os.path.isfile(os.path.join(PVFMM_DIR, "MakeVariables")):
    raise FileNotFoundError("Cannot locate MakeVariables at %s. "
                            "Please check whether PVFMM_DIR "
                            "is set up correctly." % PVFMM_DIR)

with open(os.path.join(PVFMM_DIR, "MakeVariables"), 'r') as mvfp:
    PVFMM_CONFIG = mvfp.read()


def parse_makevars(makevars):
    """Extract variable definitions from MakeVariables.
    """
    makevardef = re.compile('^([a-zA-Z0-9_]+)[ ]*=(.*)')
    variables = dict()
    for line in makevars.split('\n'):
        match = makevardef.match(line)
        if match is None:
            continue
        name, value = match.group(1, 2)

        # Strip trailing comment
        i = str.find(value, '#')
        if i >= 0:
            value = value[:i]

        value = str.strip(value)
        variables[name] = value

    return variables


def propagate_makevars(variables):
    """Propagate variables, one at a time.
    """
    var_pattern = re.compile(r'(\$\([A-Z,_]*\))')
    first_match = None
    for key, val in variables.items():
        matches = re.findall(var_pattern, val)
        if matches:
            first_match = matches[0]
            matched_key = key
            break
    if first_match:
        var_name = first_match[2:-1]
        if var_name in variables.keys():
            variables[matched_key] = variables[
                matched_key].replace(
                    first_match, variables[var_name])
        else:
            raise RuntimeError("Variable %s cannot be resolved" % var_name)

    return variables


def flatten_makevars(variables):
    """Flatten variable definitions.
    """
    n_iter = 0
    new_variables, old_variables = variables.copy(), variables.copy()
    while n_iter == 0 or (new_variables != old_variables):
        n_iter += 1
        old_variables, new_variables = \
                new_variables.copy(), propagate_makevars(new_variables)
        if n_iter > 500:
            raise RuntimeError("Too many variables substitutions!")
    return new_variables


PVFMM_MAKEVARS = flatten_makevars(parse_makevars(PVFMM_CONFIG))

PVFMM_COMPILE_ARGS = PVFMM_MAKEVARS['CXXFLAGS_PVFMM'].strip().split(' ')
PVFMM_LINK_ARGS = PVFMM_MAKEVARS['LDLIBS_PVFMM'].strip().split(' ')

INCL_PATTERN = re.compile('-I.*')
PVFMM_INCLUDE_DIR = [val[2:] for val in
                     filter(INCL_PATTERN.search, PVFMM_COMPILE_ARGS)]

MPI_COMPILE_ARGS = os.popen("mpic++ --showme:compile").read().strip().split(' ')
MPI_LINK_ARGS = os.popen("mpic++ --showme:link").read().strip().split(' ')

# }}} End setup pvfmm include and linker flags


# {{{ setup pybind11 include


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

# }}} End setup pybind11 include


# {{{ setup CXX compiler


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.

    The newer version is prefered over c++11 (when it is available).
    """
    flags = ['-std=c++17', '-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag):
            return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts + MPI_COMPILE_ARGS
            ext.extra_link_args = MPI_LINK_ARGS + PVFMM_LINK_ARGS + link_opts
        build_ext.build_extensions(self)

# }}} End setup CXX compiler


EXT_MODULES = [
    Extension(
        'pypvfmm',
        language='c++',
        sources=['src/pypvfmm.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            *PVFMM_INCLUDE_DIR
        ],
    ),
]


def main():
    """By default a bundled version of pvfmm is built, which requires
    autotools. User can also specify to build against an existing pvfmm
    installation by setting the PVFMM_DIR environment variable to point
    to the path containing the MakeVariables file.
    """
    ver_dic = get_version()

    setup(name="pypvfmm",
          version=ver_dic["VERSION_TEXT"],
          description="Python wrappers for Dhairya Malhotra's pvfmm library",
          long_description=open("README.rst", "rt").read(),
          author="Xiaoyu Wei",
          author_email="xywei@pm.me",
          license="wrapper: MIT/pvfmm: LGPLv3",
          install_requires=['pybind11'],
          setup_requires=['pybind11'],
          url="http://github.com/xywei/pypvfmm",
          ext_modules=EXT_MODULES,
          cmdclass={'build_ext': BuildExt},
          zip_safe=False,
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
