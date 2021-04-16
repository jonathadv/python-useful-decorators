MODULE_NAME = decorators
TEST_DIR = tests

default: help

upgrade-dist-tools:
	pipenv run python -m pip install --upgrade setuptools wheel twine

# Install packages from Pipfile
install:
	pipenv install

# Install packages and dev packages from Pipfile
install-dev:
	pipenv install --dev

# Install packages from Pipfile.lock
sync:
	pipenv sync

# Run pylint
lint:
	pipenv run pylint $(MODULE_NAME)


# Run tests with pytest
test:
	pipenv run pytest


# Run tests with pytest and coverage
test-cov:
	pipenv run pytest --cov-report term-missing --cov=$(MODULE_NAME)


# Create wheel from source
build: upgrade-dist-tools
	pipenv run python setup.py sdist bdist_wheel


# Remove build files
clean:
	rm -rf build/ *.egg-info/ dist/

# Sort imports as PEP8
isort:
	pipenv run isort **/*.py

# Format with black
format:
	pipenv run black $(MODULE_NAME) $(TEST_DIR)


# Upload dist content to test.pypi.org
upload-test:
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*


# Upload dist content to pypi.org
upload:
	pipenv run twine upload  dist/*

# Display this help
help:
	@ echo
	@ echo '  Usage:'
	@ echo ''
	@ echo '	make <target> [flags...]'
	@ echo ''
	@ echo '  Targets:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?:/{ print "   ", $$1, comment }' ./Makefile | column -t -s ':' | sort
	@ echo ''
	@ echo '  Flags:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?\?=/{ print "   ", $$1, $$2, comment }' ./Makefile | column -t -s '?=' | sort
	@ echo ''