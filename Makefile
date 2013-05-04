test:
	python3 zeta.py < tests/simple.lisp | diff tests/simple.out -
	python3 zeta.py < tests/library.lisp | diff tests/library.out -
	@echo "Tests passed"

loud:
	python3 zeta.py < tests/simple.lisp
	python3 zeta.py < tests/library.lisp

update:
	@echo "Generating new test output"
	python3 zeta.py < tests/simple.lisp > tests/simple.out
	python3 zeta.py < tests/library.lisp > tests/library.out

clean:
	rm -rf src/*.pyc src/__pycache__
