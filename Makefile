.PHONY: test
PROJECT=nixie
PYTHON=python

test:
	$(PYTHON) -m unittest -v tests.test_nixie
