pycodestyle:
	@flake8 .

test: pycodestyle
	@DATABASE_URI=sqlite:/// py.test tests/

test-debug:
	@DATABASE_URI=sqlite:/// py.test tests/ --pdb
