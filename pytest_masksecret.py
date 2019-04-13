# -*- coding: utf-8 -*-

import sys

import pytest
from _pytest import capture, compat

capture.capture_fixtures.update({'capsecret'})

def pytest_addoption(parser):
    group = parser.getgroup('masksecret')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2019',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo

class SysCapture(object):
    """TO DELETE: from _pytest.capture.SysCapture"""
    EMPTY_BUFFER = str()

    def __init__(self, fd, tmpfile=None):
        name = capture.patchsysdict[fd]
        self._old = getattr(sys, name)
        self.name = name
        if tmpfile is None:
            if name == "stdin":
                tmpfile = capture.DontReadFromInput()
            else:
                tmpfile = compat.CaptureIO()
        self.tmpfile = tmpfile

    def start(self):
        setattr(sys, self.name, self.tmpfile)

    def snap(self):
        res = self.tmpfile.getvalue()
        self.tmpfile.seek(0)
        self.tmpfile.truncate()
        return res

    def done(self):
        setattr(sys, self.name, self._old)
        del self._old
        capture._attempt_to_close_capture_file(self.tmpfile)

    def suspend(self):
        setattr(sys, self.name, self._old)

    def resume(self):
        setattr(sys, self.name, self.tmpfile)

    def writeorg(self, data):
        self._old.write(data)
        self._old.flush()

class SecretCapture(object):
    """TODO"""
    def __init__(self, fd, tmpfile=None):
        name = capture.patchsysdict[fd]
        self._old = getattr(sys, name)
        self.name = name

@pytest.fixture
def capsecret(request):
    """scrub the test report for registered secrets"""
    capture._ensure_only_one_capture_fixture(request, 'capsecret')
    with capture._install_capture_fixture_on_item(request, SecretCapture) as fixture:
        yield fixture
