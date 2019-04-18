# -*- coding: utf-8 -*-

import random
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


SECRETS_LIST = dict()
class ExtendedCaptureFixture(capture.CaptureFixture):
    def register_secret(self, secret, obscuring_text=''):
        """adds secret + obscuring_text to internal secrets_list tracking

        Args:
            secret (str): text to obscure
            obscuring_text (str): custom text to replace secret text with

        """
        # self._secrets_list.update({secret:'*' * random.randint(8, 32)})
        SECRETS_LIST.update({secret:obscuring_text or '*' * random.randint(8, 32)})

    def dump_secret(self):
        return SECRETS_LIST

BaseCaptureFixture = capture.CaptureFixture
class SecretCapture(capture.SysCapture):
    """TODO"""
    def writeorg(self, data):
        # for secret, blob in self._secrets_list.items():
        for secret, blob in SECRETS_LIST.items():
            data.replace(secret, blob)
        # print(f'SECRETCAPTURE: `{dir(data)}`')
        self._old.write(data)
        self._old.flush()

    def snap(self):
        res = self.tmpfile.getvalue()
        for secret, blob in SECRETS_LIST.items():
            res = res.replace(secret, blob)
        self.tmpfile.seek(0)
        self.tmpfile.truncate()
        return res

    def register_secret(self, secret, obscuring_text=''):
        """adds secret + obscuring_text to internal secrets_list tracking

        Args:
            secret (str): text to obscure
            obscuring_text (str): custom text to replace secret text with

        """
        # self._secrets_list.update({secret:'*' * random.randint(8, 32)})
        SECRETS_LIST.update({secret:'*' * random.randint(8, 32)})


    def pop_outerr_to_orig(self):
        """ pop current snapshot out/err capture and flush to orig streams. """
        out, err = self.readouterr()
        if out:
            self.out.writeorg(out)
        if err:
            self.err.writeorg(err)
        return out, err


@pytest.fixture
def capsecret(request):
    """scrub the test report for registered secrets"""
    capture._ensure_only_one_capture_fixture(request, 'capsecret')
    capture.CaptureFixture = ExtendedCaptureFixture
    with capture._install_capture_fixture_on_item(request, SecretCapture) as fixture:
        yield fixture
    capture.CaptureFixture = BaseCaptureFixture
