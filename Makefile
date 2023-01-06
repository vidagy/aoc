TEST_FILTER_ARG=$(if $(TEST_FILTER),-k "$(TEST_FILTER)",)
PYTHON=python3.9

.PHONY: run
run:
	$(PYTHON) run.py

.PHONY: next
next:
	$(PYTHON) next.py

.PHONY: profile
profile:
	$(PYTHON) -m cProfile -o /tmp/tmp.prof run.py
	snakeviz /tmp/tmp.prof

# Tests

.PHONY: test
test: unit-test

.PHONY: unit-test
unit-test:
	$(PYTHON) -m pytest ./tests/unit $(TEST_FILTER_ARG)

# Lint

.PHONY: lint
lint: format check

.PHONY: format
format: isort black

.PHONY: isort
isort:
	@echo -e "\033[0;36mFormatting files [isort] \033[0m"
	@$(PYTHON) -m isort aoc/ tests/ run.py next.py

.PHONY: black
black:
	@echo -e "\033[0;36mFormatting files [black] \033[0m"
	@$(PYTHON) -m black aoc/ tests/ run.py next.py

.PHONY: check
check: mypy flake8

.PHONY: mypy
mypy:
	@echo -e "\033[0;36mLinting files [mypy] \033[0m"
	@$(PYTHON) -m mypy aoc/ run.py next.py

.PHONY: flake8
flake8:
	@echo -e "\033[0;36mLinting files [flake8] \033[0m"
	@$(PYTHON) -m flake8 aoc/ tests/ run.py next.py
