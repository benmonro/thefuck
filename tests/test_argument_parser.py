import pytest
from therandy.argument_parser import Parser
from therandy.const import ARGUMENT_PLACEHOLDER


def _args(**override):
    args = {'alias': None, 'command': [], 'yes': False,
            'help': False, 'version': False, 'debug': False,
            'force_command': None, 'repeat': False,
            'enable_experimental_instant_mode': False,
            'shell_logger': None}
    args.update(override)
    return args


@pytest.mark.parametrize('argv, result', [
    (['therandy'], _args()),
    (['therandy', '-a'], _args(alias='randy')),
    (['therandy', '--alias', '--enable-experimental-instant-mode'],
     _args(alias='randy', enable_experimental_instant_mode=True)),
    (['therandy', '-a', 'fix'], _args(alias='fix')),
    (['therandy', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch'], yes=True)),
    (['therandy', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch', '-a'], yes=True)),
    (['therandy', ARGUMENT_PLACEHOLDER, '-v'], _args(version=True)),
    (['therandy', ARGUMENT_PLACEHOLDER, '--help'], _args(help=True)),
    (['therandy', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y', '-d'],
     _args(command=['git', 'branch', '-a'], yes=True, debug=True)),
    (['therandy', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-r', '-d'],
     _args(command=['git', 'branch', '-a'], repeat=True, debug=True)),
    (['therandy', '-l', '/tmp/log'], _args(shell_logger='/tmp/log')),
    (['therandy', '--shell-logger', '/tmp/log'],
     _args(shell_logger='/tmp/log'))])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
