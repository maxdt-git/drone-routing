CONFIG = config.txt
MAIN = parsing/parse.py


# install:

run:
	python3 $(MAIN) $(CONFIG)

debug:
	python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 . --exclude=pacman_venv
	mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


.PHONY: install run debug clean lint
