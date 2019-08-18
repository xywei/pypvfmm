/* ---------------------------------------------------------------------
**
** Copyright (C) 2019 Xiaoyu Wei
**
** Permission is hereby granted, free of charge, to any person obtaining a copy
** of this software and associated documentation files (the "Software"), to deal
** in the Software without restriction, including without limitation the rights
** to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
** copies of the Software, and to permit persons to whom the Software is
** furnished to do so, subject to the following conditions:
** 
** The above copyright notice and this permission notice shall be included in
** all copies or substantial portions of the Software.
** 
** THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
** IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
** FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
** AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
** LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
** OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
** THE SOFTWARE.
**
** -------------------------------------------------------------------*/

namespace pypvfmm{

  enum KernelKind {
    LaplacePotential = 1,
    LaplaceGradient  = 3,

    StokesVelocity   = 5,
    StokesPressure   = 7,
    StokesStress     = 9,
    StokesVelGrad    = 11,

    BiotSavartPotential = 13,

    HelmholtzPotential  = 15,
  };

  const std::unordered_map<std::string, KernelKind>
    kernel_map{
      {"LaplaceKernel, potential", KernelKind::LaplacePotential},
      {"LapKnl3D",                 KernelKind::LaplacePotential},
      {"LaplaceKernel, gradient",  KernelKind::LaplaceGradient},

      {"StokesKernel, velocity", KernelKind::StokesVelocity},
      {"StokesKernel, pressure", KernelKind::StokesPressure},
      {"StokesKernel, stress",   KernelKind::StokesStress},
      {"StokesKernel, vel_grad", KernelKind::StokesVelGrad},

      {"BiotSavartKernel, potential", KernelKind::BiotSavartPotential},

      {"HelmholtzKernel, potential", KernelKind::HelmholtzPotential},
      {"HelmKnl3D(k)",               KernelKind::HelmholtzPotential},
    };

  template <class T>
    const pvfmm::Kernel<T> get_kernel(const std::string &kernel_desc) {
      auto query = kernel_map.find(kernel_desc);
      if (query == kernel_map.end()) {
        throw std::runtime_error("Invalid kernel_desc: " + kernel_desc);
      }
      auto kind = query->second;

      switch(kind) {
        case KernelKind::LaplacePotential:
          return pvfmm::LaplaceKernel<T>::potential();
        case KernelKind::LaplaceGradient:
          return pvfmm::LaplaceKernel<T>::gradient();

        case KernelKind::StokesVelocity:
          return pvfmm::StokesKernel<T>::velocity();
        case KernelKind::StokesPressure:
          return pvfmm::StokesKernel<T>::pressure();
        case KernelKind::StokesStress:
          return pvfmm::StokesKernel<T>::stress();
        case KernelKind::StokesVelGrad:
          return pvfmm::StokesKernel<T>::vel_grad();

        case KernelKind::BiotSavartPotential:
          return pvfmm::BiotSavartKernel<T>::potential();

        case KernelKind::HelmholtzPotential:
          return pvfmm::HelmholtzKernel<T>::potential();
      }
    }

} // end of namespace pypvfmm
