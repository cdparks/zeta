test:
	python3 zeta.py < tests/test.lisp | diff tests/test.out -
	@echo "Tests passed"

clean:
	rm -rf src/*.pyc src/__pycache__
