.PHONY: docs

docs:
	cd docs; make html

clean-docs:
	@echo "Cleaning docs"
	cd docs; make -i clean

clean: clean-docs
