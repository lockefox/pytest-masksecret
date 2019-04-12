# -*- coding: utf-8 -*-

import pytest
from _pytest import capture


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

@pytest.fixture
def capsecret(request):
    """scrub the test report for registered secrets"""
