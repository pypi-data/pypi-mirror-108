#!/bin/bash -eu

TARGET_PYTHON_VERSION=3.7

function main() {
  if ! has_target_python_version_installed
  then
    echo "Installing latest Python ${TARGET_PYTHON_VERSION} version"
    pyenv install -s "$(find_latest_target_python_version_available)"
  fi

  pushd "$(dirname "$0")/../python" > /dev/null

  if test -f ".python-version"
  then
    echo "Directory $(pwd) already configured to use $(cat .python-version)"
  else
    local python_version_to_use=$(find_latest_target_python_version_installed)
    echo "Marking $(pwd) to use Python $python_version_to_use"
    pyenv local "$python_version_to_use"
  fi

  popd > /dev/null
}

function has_target_python_version_installed() {
  pyenv versions | \
    grep -q $TARGET_PYTHON_VERSION
}

function find_latest_target_python_version_available() {
  pyenv install --list | find_latest_target_python_version_in_list
}

function find_latest_target_python_version_installed() {
  pyenv versions | find_latest_target_python_version_in_list
}

function find_latest_target_python_version_in_list() {
  grep -oE "${TARGET_PYTHON_VERSION}\.[0-9]+" |
    sort -V |
    tail -1
}

main
