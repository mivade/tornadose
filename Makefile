.PHONY: docs build

build:
	python setup.py bdist_wheel

docs:
	cd docs; make html

test:
	py.test

clean-docs:
	@echo "Cleaning docs"
	cd docs; make -i clean

clean-py:
	@echo "Cleaning builds"
	rm -rf build/
	rm -rf dist/
	rm -rf tornadose.egg-info/
	rm -rf htmlcov/

clean: clean-py clean-docs
