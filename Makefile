.PHONY: docs build

build:
	python setup.py sdist
	python setup.py bdist_wheel

docs:
	cd docs; make html

black:
	black tornadose/ tests/ setup.py

test:
	pytest --html=test-report.html --self-contained-html

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
