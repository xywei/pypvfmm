#include <mpi.h>
#include <omp.h>
#include <iostream>

${pvfmm_headers}
${pybind11_headers}

${template_instantiations}

PYBIND11_MODULE(wrapper, m) {

  m.doc() = "${wrapper_doc}";

  auto mprecomp_mat = m.def_submodule("precomp_mat");
  pybind11::class_<pvfmm::PrecompMat<double>>(mprecomp_mat, "PrecompMat")
    .def(pybind11::init<bool>(), pybind11::arg("scale_invar"));

}

// vim: ft=cpp
