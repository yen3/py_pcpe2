#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <string>
#include <vector>

int add(int i, int j) {
    return i + j;
}

int subtract(int i, int j) {
    return i - j;
}

void print_string(std::string& s) {
  std::cout << s << std::endl;
}

std::string return_the_same_string(std::string& s) {
  std::string s1(s);
  return s1;
}

std::vector<std::string> add_string_suffix(std::vector<std::string>& ss) {
  std::vector<std::string> rs;

  for (const auto& s : ss) {
    rs.emplace_back(s + "_cpp11");
  }

  return rs;
}


namespace py = pybind11;

PYBIND11_PLUGIN(pcpe2_core) {
    py::module m("pcpe2_core", R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: pcpe2_core

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc");

    m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

    m.def("subtract", &subtract, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");

    m.def("print_str", &print_string, R"pbdoc(
      Print a string to stdout.
    )pbdoc");

    m.def("return_str", &return_the_same_string, R"pbdoc(
      Return the same string.
    )pbdoc");

    m.def("add_str_list_suffix", &add_string_suffix, R"pbdoc(
      Return the list of string with suffix.
    )pbdoc");

    m.def("add_str_list_suffix2",
        [](const std::vector<std::string>& ss) -> std::vector<std::string> {
          std::vector<std::string> rs;

          for (const auto& s : ss) {
            rs.emplace_back(s + "_cpp11");
          }

          return rs;
        }, R"pbdoc(
      Return the list of string with suffix.
    )pbdoc");




#ifdef VERSION_INFO
    m.attr("__version__") = py::str(VERSION_INFO);
#else
    m.attr("__version__") = py::str("dev");
#endif

    return m.ptr();
}
