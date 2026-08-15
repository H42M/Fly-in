PYTHON = python3
REQUIREMENTS = requirements.txt
MAIN = fly-in.py
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python

.PHONY: install run visualizer debug clean lint lint-strict

$(VENV_PYTHON):
	@$(PYTHON) -m venv $(VENV)

install: $(VENV_PYTHON)
	@$(VENV_PYTHON) -m pip install --upgrade pip
	@$(VENV_PYTHON) -m pip install -r $(REQUIREMENTS)

run:
	@if [ ! -x "$(VENV_PYTHON)" ]; then \
		echo "Error: virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@$(VENV_PYTHON) $(MAIN)

debug: install
	@$(VENV_PYTHON) -m pdb $(MAIN)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .mypy_cache .pytest_cache

fclean: clean
	@rm -rf $(VENV)

re: fclean install

lint:
	@$(VENV_PYTHON) -m flake8 . --exclude=.venv
	@$(VENV_PYTHON) -m mypy . --exclude '^\.venv/' --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	@$(VENV_PYTHON) -m flake8 . --exclude=.venv
	@$(VENV_PYTHON) -m mypy . --exclude '^\.venv/' --strict \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs