#include <mpi.h>
#include <omp.h>
#include <iostream>

#include <precomp_mat.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

template class pvfmm::PrecompMat<double>;

PYBIND11_MODULE(pypvfmm, m) {

  py::class_<pvfmm::PrecompMat<double>>(m, "PrecompMat")
    .def(py::init<bool>(), py::arg("scale_invar"));

}
