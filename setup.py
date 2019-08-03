#!/usr/bin/env python

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


def main():

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
              'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
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
