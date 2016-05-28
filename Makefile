.PHONY: docs

docs:
	cd docs; make html

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
