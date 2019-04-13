VENV_FILE=.venv
WHICH_PYTHON=${VENV_FILE}/bin/python
WHICH_PIP=${VENV_FILE}/bin/pip

clean:
	-@rm -rf $(VENV_FILE)
	-@rm -rf .eggs
	-@rm -rf *.egg-info
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
~.pyenv/versions/3.7.3: /usr/local/bin/pyenv
	-@pyenv install 3.7.3
~.pyenv/versions/3.6.7: /usr/local/bin/pyenv
	-@pyenv install 3.6.7
else
~.pyenv/versions/3.7.3: 
	-@pyenv install 3.7.3
~.pyenv/versions/3.6.7: 
	-@pyenv install 3.6.7
endif

.PHONY: pyenv-local
pyenv-local: ~.pyenv/versions/3.7.3 ~.pyenv/versions/3.6.7
	@pyenv local 3.7.3
	@pyenv local 3.6.7
	@eval "$(pyenv init -)"

$(VENV_FILE):
	@virtualenv $(VENV_FILE) -p python3

$(VENV_FILE)/lib/python*/site-packages/tox/:
	@${WHICH_PIP} install tox

$(VENV_FILE)/lib/python*/site-packages/tox-pyenv/:
	@${WHICH_PIP} install tox

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
