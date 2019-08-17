#include <mpi.h>
#include <omp.h>
#include <iostream>
#include <any>
#include <array>
#include <vector>
#include <string>
#include <unordered_map>

${pvfmm_headers}
${pybind11_headers}

${numpy_wrappers}

${template_instantiations}

PYBIND11_MODULE(wrapper, m) {

  m.doc() = "${wrapper_doc}";

  // submodules
${wrapper_submodules}

  // class wrappers
${wrapper_classes}

  // function wrappers
${wrapper_functions}

}

// vim: ft=cpp
