import re
import subprocess
from therandy import utils
from therandy.utils import replace_argument
from therandy.specific.git import git_support
from therandy.shells import shell


@git_support
def match(command):
    return ('did not match any file(s) known to git.' in command.output
            and "Did you forget to 'git add'?" not in command.output)


def get_branches():
    proc = subprocess.Popen(
        ['git', 'branch', '-a', '--no-color', '--no-column'],
        stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
        line = line.decode('utf-8')
        if line.startswith('*'):
            line = line.split(' ')[1]
        if '/' in line:
            line = line.split('/')[-1]
        yield line.strip()


@git_support
def get_new_command(command):
    missing_file = re.findall(
        r"error: pathspec '([^']*)' "
        r"did not match any file\(s\) known to git.", command.output)[0]
    closest_branch = utils.get_closest(missing_file, get_branches(),
                                       fallback_to_first=False)
    if closest_branch:
        return replace_argument(command.script, missing_file, closest_branch)
    elif command.script_parts[1] == 'checkout':
        return replace_argument(command.script, 'checkout', 'checkout -b')
    else:
        return shell.and_('git branch {}', '{}').format(
            missing_file, command.script)
