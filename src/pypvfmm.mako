#include <mpi.h>
#include <omp.h>
#include <iostream>

${pvfmm_headers}
${pybind11_headers}

namespace py = pybind11;

${template_instantiations}

PYBIND11_MODULE(wrapper, m) {

  py::class_<pvfmm::PrecompMat<double>>(m, "PrecompMat")
    .def(py::init<bool>(), py::arg("scale_invar"));

}

// vim: ft=cpp
