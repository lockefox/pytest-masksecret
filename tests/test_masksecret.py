# -*- coding: utf-8 -*-
import pytest

@pytest.mark.local
def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_sth(bar):
            assert bar == "europython2015"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--foo=europython2015',
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

@pytest.mark.local
def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'masksecret:',
        '*--foo=DEST_FOO*Set the value for the fixture "bar".',
    ])

@pytest.mark.local
def test_hello_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        HELLO = world
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

@pytest.mark.local
def test_capsecret_happypath(testdir):
    testdir.makepyfile("""
        import pytest

        def fake_func(arg):
            print(arg)
            raise Exception

        def test_capsecret(capsecret):
            capsecret.register_secret('bob')
            print(capsecret.dump_secret())
            print('hello bob')
            assert False

        def test_nosecret(capsys):
            print('hello bob')
            assert False

        def test_capsecret_func(capsecret):
            fake_func('bob')

    """)
    result = testdir.runpytest('-v', '--tb=native')
    print(f'\n~~~\nRESULT: `{result.outlines}`\n~~~\n')
    assert False
