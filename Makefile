test:
	python zeta.py < tests/test.lisp | diff tests/test.out -
	@echo "Tests passed"

clean:
	rm -f src/*.pyc
