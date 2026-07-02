PYTHON = python3
REQUIREMENTS = requirements.txt
MAIN = fly-in.py


install:
	$(PYTHON) -m pip install -r REQUIREMENTS

run:
	@$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	rm -rf __pycache__ .mypy__cache

lint:
	@flake8 .
	@mypy . --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	@flake8 .
	@mypy . --strict \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs