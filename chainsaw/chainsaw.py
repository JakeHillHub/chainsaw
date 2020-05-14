"""chainsaw main"""

import os
import re
import sys
import json
import shutil
import argparse
import subprocess


__VERSION__ = '0.1.0'


def cmd(string, cwd=os.getcwd(), verbose=True, shell=False):
    """Wraps Popen"""

    if not shell:  # Split command up by spaces
        string = string.split(' ')

    process = subprocess.Popen(string, cwd=cwd, stdout=subprocess.PIPE, shell=shell)
    to_string = process.communicate()[0].decode('utf-8')
    if verbose:
        try:
            print(to_string)
        except BrokenPipeError:
            pass
    return to_string


def filter_none(args):
    """Takes a list of args and removes None values"""

    return list(filter(lambda x: x != None, args))


def filter_subtrees(prefixes, subtrees, invert=False):
    """Takes the json list of subtrees and returns only the ones specified (by prefix)"""

    if invert:
        return list(filter(lambda subt: subt['prefix'] not in prefixes, subtrees))

    return list(filter(lambda subt: subt['prefix'] in prefixes, subtrees))


def all_prefixes(subtrees):
    """Get all prefixes as a list from subtrees"""

    return [subt['prefix'] for subt in subtrees]


def load_json():
    """Attempts to load a file in the current directory called chainsaw.json"""

    if not os.path.isfile('chainsaw.json'):
        print('no chainsaw.json file found, add a subtree with "chainsaw add" or create a chainsaw.json definition from scratch')
        sys.exit(0)

    with open('chainsaw.json', 'r') as file:
        loaded_json = json.load(file)
        return loaded_json if loaded_json else []  # Return empty list if chainsaw.json is empty


def add_subtree_to_json(subtree):
    """Attempts to add a given subtrees information to the chainsaw.json file"""

    if not os.path.isfile('chainsaw.json'):
        with open('chainsaw.json', 'w') as file:
            file.write(json.dumps([], sort_keys=True, indent=4, separators=(',', ': ')))

    chainsaw_json = load_json()
    chainsaw_json.append(subtree)
    with open('chainsaw.json', 'w') as file:
        file.write(json.dumps(chainsaw_json, sort_keys=True, indent=4, separators=(',', ': ')))


def overwrite_subtree_json(subtrees):
    """Completely overwrite existing chainsaw.json file"""

    with open('chainsaw.json', 'w') as file:
        file.write(json.dumps(subtrees, sort_keys=True, indent=4, separators=(',', ': ')))


def add(args):
    """Add subtree and update chainsaw.json"""

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


def pull(args):
    """Pull and merge using subtree strategy from subtree remote"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--all', dest='all', action='store_true', help='Update all subtrees')
    parser.add_argument('--squash', dest='squash', action='store_true', help='Squash subtree history into one commit')
    parser.add_argument('prefixes', nargs='*', default=[], help='Subtree prefixes/paths')
    args = parser.parse_args(args)

    subtrees = load_json()
    subtrees = filter_subtrees(all_prefixes(subtrees) if args.all else args.prefixes, subtrees)

    for subt in subtrees:
        command = 'git subtree pull -P {} {} {}'.format(subt['prefix'], subt['remote'], subt['branch'])
        if args.squash:
            command += ' --squash'
        cmd(command)


def push(args):
    """Push changes to subtree remote"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--all', dest='all', action='store_true', help='Push all changes in subtrees')
    parser.add_argument('prefixes', nargs='*', default=[], help='Subtree prefixes/paths')
    args = parser.parse_args(args)

    subtrees = load_json()
    subtrees = filter_subtrees(all_prefixes(subtrees) if args.all else args.prefixes, subtrees)

    for subt in subtrees:
        cmd('git subtree push -P {} {} {}'.format(subt['prefix'], subt['remote'], subt['branch']))


def reset(args):
    """Reset a specific subtree to specific commit"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--squash', action='store_true', help='Squash subtree history into one commit')
    parser.add_argument('prefix', help='Subtree prefix/path')
    parser.add_argument('commit', help='Commit hash to reset to')
    args = parser.parse_args(args)

    subtrees = load_json()
    subt = filter_subtrees([args.prefix], subtrees)[0]

    command = 'git subtree merge -P {} {}'.format(subt['prefix'], args.commit)
    if args.squash:
        command += ' --squash'
    cmd(command)


def merge(args):
    print('Merge not implemented')
    pass


def remove(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true', help='Remove all subtrees')
    parser.add_argument('prefixes', nargs='*', default=[], help='Subtree prefixes/paths')
    args = parser.parse_args(args)

    subtrees = load_json()
    fsubtrees = filter_subtrees(all_prefixes(subtrees) if args.all else args.prefixes, subtrees)

    for subt in fsubtrees:
        cmd('git rm -rf {}'.format(subt['prefix']))

    overwrite_subtree_json(filter_subtrees(all_prefixes(fsubtrees), subtrees, invert=True))


def ls(args):
    """List existing submodules using git log"""

    for line in cmd('git log', verbose=False).split('\n'):
        if re.search('git-subtree-dir', line):
            print(line.split(' ')[-1])


def graph(args):
    """Display git history in graph form (not really specific to subtree but whatever)"""

    cmd('git -c color.ui=always log --graph --abbrev-commit --decorate --oneline')


def cs_help(args):
    """Display help for a specific action"""

    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='Help action')
    help_args = parser.parse_args(args)

    if help_args.action in ACTIONS.keys():
        ACTIONS[help_args.action](['--help'])
    else:
        ACTIONS['unknown'](f'no action named: {help_args.action}')


ACTIONS = {
    'pull': pull,
    'add': add,
    'push': push,
    'reset': reset,
    'merge': merge,
    'remove': remove,
    'rm': remove,
    'ls': ls,
    'graph': graph,
    'help': cs_help,
    'version': lambda _: print(f'git-chainsaw version {__VERSION__}'),
    'unknown': lambda args: print(f'invalid command {args}')
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', help='Subtree Action: {}'.format(' '.join(ACTIONS.keys())))
    known, action_args = parser.parse_known_args()

    if known.action in ACTIONS.keys():
        ACTIONS[known.action](action_args)
    else:
        ACTIONS['unknown'](f'no action named: {known.action}')


if __name__ == '__main__':
    main()
