.PHONY: docs build

build:
	python setup.py sdist
	python setup.py bdist_wheel

docs:
	cd docs; make html

test:
	pytest

clean-docs:
	@echo "Cleaning docs"
	cd docs; make -i clean

clean-py:
	@echo "Cleaning builds"
	rm -rf build/
	rm -rf dist/
	rm -rf tornadose.egg-info/
	rm -rf htmlcov/
	rm -rf `find . -name *.pyc`
	rm -rf `find . -name __pycache__`

clean: clean-py clean-docs
