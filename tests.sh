echo "Pylint"
pylint src/ --rcfile=.pylintrc

echo ""
echo "Unittests"
python -m unittest discover

