#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <string>
#include <vector>
#include <map>

#include "com_subseq_sort.h"
#include "small_seq_hash.h"
#include "max_comsubseq.h"
#include "env.h"
#include "pcpe_util.h"
#include "logging.h"

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

    m.def("env_get_compare_seq_size", [](){
          return pcpe::gEnv.getCompareSeqenceSize();
        },
        R"pbdoc(
          Get the compare sequence size
        )pbdoc");

    m.def("env_set_compare_seq_size", [](uint32_t set_size){
          pcpe::gEnv.setCompareSeqenceSize(set_size);
        },
        R"pbdoc(
         Set the compare sequence size
        )pbdoc");

    m.def("env_get_thread_size", [](){
          return pcpe::gEnv.getThreadsSize();
        },
        R"pbdoc(
          Get the thread size
        )pbdoc");

    m.def("env_set_thread_size", [](uint32_t set_size){
          pcpe::gEnv.setThreadSize(set_size);
        },
        R"pbdoc(
          Set the thread size
        )pbdoc");

    m.def("env_get_buffer_size", [](){
          return pcpe::gEnv.getBufferSize();
        },
        R"pbdoc(
          Get the buffer size
        )pbdoc");

    m.def("env_set_buffer_size", [](uint32_t set_size){
          pcpe::gEnv.setBufferSize(set_size);
        },
        R"pbdoc(
         Set the buffer size
        )pbdoc");

    m.def("env_get_io_buffer_size", [](){
          return pcpe::gEnv.getIOBufferSize();
        },
        R"pbdoc(
          Get the IO buffer size
        )pbdoc");

    m.def("env_set_io_buffer_size", [](uint32_t set_size){
          pcpe::gEnv.setIOBufferSize(set_size);
        },
        R"pbdoc(
          Set the IO buffer size
        )pbdoc");
    m.def("init_logging", [](uint32_t logging_level){
          std::map<uint32_t, pcpe::LoggingLevel> python_logging_map;
          python_logging_map[0] = pcpe::LoggingLevel::kNone;
          python_logging_map[10] = pcpe::LoggingLevel::kDebug;
          python_logging_map[20] = pcpe::LoggingLevel::kInfo;
          python_logging_map[30] = pcpe::LoggingLevel::kWarning;
          python_logging_map[40] = pcpe::LoggingLevel::kError;
          python_logging_map[50] = pcpe::LoggingLevel::kFatal;

          if (python_logging_map.find(logging_level) !=
              python_logging_map.end())
            pcpe::InitLogging(python_logging_map[logging_level]);
          else
            pcpe::InitLogging(pcpe::LoggingLevel::kWarning);
        },
        R"pbdoc(
          Set logging level
        )pbdoc");


    return m.ptr();
}
