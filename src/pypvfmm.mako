#include <mpi.h>
#include <omp.h>
#include <iostream>

${pvfmm_headers}
${pybind11_headers}

${template_instantiations}

PYBIND11_MODULE(wrapper, m) {

  m.doc() = "${wrapper_doc}";

  // submodules
${wrapper_submodules}

  // class wrappers
${wrapper_classes}

}

// vim: ft=cpp
