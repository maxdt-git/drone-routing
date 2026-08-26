CONFIG = maps/hard/01_maze_nightmare.txt
MAIN = main.py


venv:
	python3 -m venv fly_venv

install: venv
	fly_venv/bin/pip install flake8
	fly_venv/bin/pip install mypy

run:
	fly_venv/bin/python3 $(MAIN) $(CONFIG)

debug:
	fly_venv/bin/python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf fly_venv

lint:
	fly_venv/bin/flake8 . --exclude=fly_venv
	fly_venv/bin/mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


.PHONY: venv install run debug clean fclean lint
