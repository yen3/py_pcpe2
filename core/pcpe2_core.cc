#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "com_subseq_sort.h"
#include "small_seq_hash.h"
#include "max_comsubseq.h"
#include "env.h"
#include "pcpe_util.h"

#include <iostream>
#include <string>
#include <vector>

namespace py = pybind11;

PYBIND11_PLUGIN(pcpe2_core) {
    py::module m("pcpe2_core", R"pbdoc(
        pcpe2 core
        -----------------------

        .. currentmodule:: pcpe2_core

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc");

    m.def("env_set_temp_path", [](const std::string& path){
          pcpe::gEnv.setTempFolderPath(path);
        },
        R"pbdoc(
          Set the temp folder path
        )pbdoc");

    m.def("env_get_temp_path", [](){
          return pcpe::gEnv.getTempFolderPath();
        },
        R"pbdoc(
          Get the temp folder path
        )pbdoc");

    m.def("env_get_min_output_length", [](){
          return pcpe::gEnv.getMinimumOutputLength();
        },
        R"pbdoc(
          Get the minimum output length
        )pbdoc");

    m.def("env_set_min_output_length", [](uint32_t set_length){
          pcpe::gEnv.setMinimumOutputLength(set_length);
        },
        R"pbdoc(
          Set the minimum output length
        )pbdoc");

    m.def("compare_small_seqs",
          [](const pcpe::FilePath& xfilepath, const pcpe::FilePath& yfilepath) {
            std::vector<pcpe::FilePath> cs;
            pcpe::CompareSmallSeqs(xfilepath, yfilepath, cs);

            return cs;
          },
          R"pbdoc(
            Compare the small common subsequences with lenth 6.
          )pbdoc");

    m.def("sort_comsubseq_files",
          [](const std::vector<pcpe::FilePath>& cs) {
            std::vector<pcpe::FilePath> sorted_cs;
            pcpe::SortComSubseqsFiles(cs, sorted_cs);

            return sorted_cs;
          },
          R"pbdoc(
            Sort each file which contains lists of ComSubseq.
          )pbdoc");

    m.def("max_sorted_comsubsq_files",
          [](const std::vector<pcpe::FilePath>& sorted_cs) {
            std::vector<pcpe::FilePath> max_cs;
            pcpe::MaxSortedComSubseqs(sorted_cs, max_cs);

            return max_cs;
          },
          R"pbdoc(
            Find the maxmimum common subseqences for each sorted ComSubseq File.
          )pbdoc");

    return m.ptr();
}
