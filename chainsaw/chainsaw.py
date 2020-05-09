import os
import re
import json
import argparse
import subprocess
from io import BytesIO


__VERSION__ = '0.0.3'


def cmd(string, cwd=os.getcwd(), verbose=True):
    process = subprocess.Popen(string.split(' '), cwd=cwd, stdout=subprocess.PIPE)
    to_string = process.communicate()[0].decode('utf-8')
    if verbose:
        print(to_string)
    return to_string


def filter_none(args):
    """Takes a list of args and removes None values"""
    return list(filter(lambda x: x != None, args))


def load_json():
    """Attempts to load a file in the current directory called chainsaw.json"""
    with open('chainsaw.json', 'r') as file:
        return json.load(file)


def add_subtree_to_json(subtree):
    """Attempts to add a given subtrees information to the chainsaw.json file"""
    if not os.path.isfile('chainsaw.json'):
        with open('chainsaw.json', 'w') as file:
            file.write(json.dumps([], sort_keys=True, indent=4, separators=(',', ': ')))

    chainsaw_json = load_json()
    chainsaw_json.append(subtree)
    with open('chainsaw.json', 'w') as file:
        file.write(json.dumps(chainsaw_json, sort_keys=True, indent=4, separators=(',', ': ')))


def pull(args):
    pass


def add(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', dest='all', action='store_true', help='Add all subtrees defined in chainsaw.json')
    parser.add_argument('--squash', dest='squash', action='store_true', help='Squash subtree history into one commit')
    parser.add_argument('prefix', nargs='?', default=None, help='Specify subtree prefix (path from top level)')
    parser.add_argument('remote', nargs='?', default=None, help='Remote url of subtree')
    parser.add_argument('branch', nargs='?', default=None, help='Branch of subtree (ie. master)')
    args = parser.parse_args(args)

    if args.all:
        for subt in load_json():
            command = 'git subtree add -P {} {} {}'.format(subt['prefix'], subt['remote'], subt['branch'])
            if args.squash:
                command += ' --squash'
            cmd(command)
    elif args.prefix and args.remote and args.branch:
        command = 'git subtree add -P {} {} {}'.format(args.prefix, args.remote, args.branch)
        if args.squash:
            command += ' --squash'
        cmd(command)
        add_subtree_to_json({
            'prefix': args.prefix,
            'remote': args.remote,
            'branch': args.branch
        })
    else:
        print(parser.parse_args(['--help']))


def push(args):
    pass


def revert(args):
    pass


def merge(args):
    pass


def ls(args):
    """List existing submodules using git log"""

    for line in cmd('git log', verbose=False).split('\n'):
        if re.search('git-subtree-dir', line):
            print(line.split(' ')[-1])


ACTIONS = {
    'pull': pull,
    'add': add,
    'push': push,
    'revert': revert,
    'merge': merge,
    'ls': ls,
    'version': lambda _: print(f'git-chainsaw version {__VERSION__}')
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', help='Subtree Action: {}'.format(' '.join(ACTIONS.keys())))
    known, action_args = parser.parse_known_args()

    action = ACTIONS.get(known.action, ACTIONS['version'])

    action(action_args)


if __name__ == '__main__':
    main()
