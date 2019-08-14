#include <mpi.h>
#include <omp.h>
#include <iostream>

${pvfmm_headers}
${pybind11_headers}

${template_instantiations}

PYBIND11_MODULE(wrapper, m) {

  m.doc() = "${wrapper_doc}";

  pybind11::class_<pvfmm::PrecompMat<double>>(m, "PrecompMat")
    .def(pybind11::init<bool>(), pybind11::arg("scale_invar"));

}

// vim: ft=cpp
