#!/usr/bin/env bash

function run_test
{
  docker run --rm --name test_pypcpe2_$1 python$1 ./test_docker.sh
}

function print_result
{
  if [[ $2 -eq 0 ]]; then
      echo "Python$1: success"
  else
      echo "Python$1: fail"
  fi
}

run_test 34
TEST_34=$?

run_test 35
TEST_35=$?

run_test 36
TEST_36=$?

echo "\nTest PyPCPE2 in:"
print_result "3.4" ${TEST_34}
print_result "3.5" ${TEST_35}
print_result "3.6" ${TEST_36}
