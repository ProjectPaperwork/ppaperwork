
tar_filepath=`readlink -f ./dist/gherkin*.tar.gz`
echo "Update from : $tar_filepath"
python3 setup.py sdist bdist_wheel
# sudo pip uninstall -y $PACKAGE
pip install --upgrade $tar_filepath
pip install --upgrade $tar_filepath
