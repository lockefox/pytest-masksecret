VENV_FILE=.venv
WHICH_PYTHON=$(VENV_FILE)/bin/python
WHICH_PIP=$(VENV_FILE)/bin/pip

clean:
	-@rm -rf $(VENV_FILE)
	-@rm -rf .eggs
	-@rm -rf *.egg-info
	-@find . -type d -maxdepth 3 -name "__pycache__" -print0 | xargs -0 rm -rv
	-@rm -rf .pytest_cache
	-@rm .coverage
	-@rm -rf pytest
	-@rm -rf test/test_capture.py
	-@rm -rf .tox

# TODO: Windows: https://stackoverflow.com/a/12099167
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
# https://github.com/pyenv/pyenv/issues/1219
CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" 
/usr/local/bin/pyenv:
	@brew update
	@brew install pyenv
${HOME}/.pyenv/versions/3.7.3: /usr/local/bin/pyenv
	-@pyenv install 3.7.3
${HOME}/.pyenv/versions/3.6.7: /usr/local/bin/pyenv
	-@pyenv install 3.6.7
else
${HOME}/.pyenv/versions/3.7.3: 
	-@pyenv install 3.7.3
${HOME}/.pyenv/versions/3.6.7: 
	-@pyenv install 3.6.7
endif

.PHONY: pyenv-local
pyenv-local: ${HOME}/.pyenv/versions/3.7.3 ${HOME}/.pyenv/versions/3.6.7
	@pyenv local 3.7.3
	@pyenv local 3.6.7
	@eval "$(pyenv init -)"

$(VENV_FILE):
	@virtualenv $(VENV_FILE) -p python3

$(VENV_FILE)/lib/python*/site-packages/tox/:
	@echo $(WHICH_PIP)
	@$(WHICH_PIP) list
	@${WHICH_PIP} install tox

$(VENV_FILE)/lib/python*/site-packages/tox-pyenv/:
	@$(WHICH_PIP) install tox-pyenv

pytest/testing/test_capture.py:
	@git clone -n https://github.com/pytest-dev/pytest.git --depth 1
	@cd pytest; git checkout HEAD testing/test_capture.py

tests/test_capture.py: pytest/testing/test_capture.py
	@cp -f pytest/testing/test_capture.py tests/test_capture.py

.PHONY: venv-setup
venv-setup: $(VENV_FILE) $(VENV_FILE)/lib/python*/site-packages/tox/ $(VENV_FILE)/lib/python*/site-packages/tox-pyenv/

.PHONY: test
test: venv-setup pyenv-local tests/test_capture.py
	@tox

.PHONY: test-fast
test-fast: venv-setup pyenv-local
	@tox -e py37 -- -m "local"