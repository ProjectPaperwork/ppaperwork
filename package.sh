#!/bin/bash

BUILD_MODE=1
INSTALL_MODE=0

while [[ $# -gt 0 ]]; do
  case $1 in
    -i|--install)
        INSTALL_MODE=1
        shift # past argument
        ;;
    *)
        shift # past argument
        ;;
  esac
done


if [ $BUILD_MODE == 1 ] ; then
    python3 setup.py sdist bdist_wheel
fi;


if [ $INSTALL_MODE == 1 ] ; then

    tar_filepath=`readlink -f ./dist/gherkin*.tar.gz`
    echo "Update from : $tar_filepath"
    python3 setup.py sdist bdist_wheel
    # sudo pip uninstall -y $PACKAGE
    pip install --upgrade $tar_filepath
    pip install --upgrade $tar_filepath

fi;


