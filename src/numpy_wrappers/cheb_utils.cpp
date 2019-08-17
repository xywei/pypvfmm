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

  template <class T>
    pybind11::object cheb_poly(
        int d,
        pybind11::array_t<T, pybind11::array::c_style> in,
        int n,
        pybind11::array_t<T, pybind11::array::c_style> out){
      // check input dimensions
      if ( in.ndim() != 1 )
        throw std::runtime_error("in should be 1-D NumPy array");

      if ( out.ndim() != 1 )
        throw std::runtime_error("out should be 1-D NumPy array");

      auto inbuf = in.request();
      auto outbuf = out.request();

      T* in_ptr = (T*) inbuf.ptr;
      T* out_ptr = (T*) outbuf.ptr;

      pvfmm::cheb_poly<T>(d, in_ptr, n, out_ptr);
      return pybind11::none();
    }


  template <class T>
    pybind11::array integ(
        int m,
        pybind11::array_t<T, pybind11::array::c_style> s,
        T r, int n, const std::string &kernel_desc){

      auto kernel = get_kernel<T>(kernel_desc);

      auto sbuf = s.request();
      T* s_ptr = (T*) sbuf.ptr;

      std::vector<T> U = pvfmm::integ<T>(m, s_ptr, r, n, kernel);

      constexpr int Udim = 1;
      const std::array<size_t, Udim> Ushape = {U.size()};
      const std::array<size_t, Udim> Ustrides = {sizeof(T)};
      
      return pybind11::array(
          pybind11::buffer_info(U.data(),
            sizeof(T), pybind11::format_descriptor<T>::value,
            Udim, Ushape, Ustrides)
          );
    }



} // end of namespace pypvfmm
