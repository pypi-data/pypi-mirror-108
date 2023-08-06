#include <pybind11/cast.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

#include "MathParser/include/parser.hpp"

namespace py = pybind11;


PYBIND11_MODULE(InfixParser, m){

  // Select non-cache accessing function

  double (MathParser::*e)(mp_RPN) = &MathParser::eval;
  e = nullptr;
  e = &MathParser::eval;

  // Construct Python Classes & Functions

  py::class_<mp_RPN>(m, "mp_RPN")
    .def_readwrite("RPN", &mp_RPN::RPN)
    .def_readwrite("RPN_values", &mp_RPN::RPNValues);

  m.def("evaluate", &evaluate);

  py::class_<MathParser>(m, "Parser")
    .def(py::init())
    .def("append_variable", &MathParser::appendVariable)
    .def("delete_variable", &MathParser::deleteVariable)
    .def("reverse_polish_notation", &MathParser::reversePolishNotation, py::arg("infix"), py::arg("_do_cache") = false)
    .def("eval", e);
}
