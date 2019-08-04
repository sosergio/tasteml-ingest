HOST=127.0.0.1
TEST_PATH=./

clean-pyc:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

run:
	python3 ingest/main.py
