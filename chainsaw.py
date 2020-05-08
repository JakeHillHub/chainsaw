import os
import json
import argparse
import subprocess


def wait_subprocess(p):
    (output, stderr) = p.communicate()
    p.wait()
    if output:
        print(output)
    if stderr:
        print(stderr)
    return output


def cmd(*args, cwd=os.getcwd()):
    return wait_subprocess(subprocess.Popen(args, cwd=cwd))


def git(*args, cwd=os.getcwd()):
    print(args)
    return cmd(*('git',) + args, cwd=cwd)


def subtree(*args, cwd=os.getcwd()):
    return git(*('subtree',) + args, cwd=cwd)


def filter_none(args):
    """Takes a list of args and removes None values"""
    return list(filter(lambda x: x != None, args))


def load_json():
    """Attempts to load a file in the current directory called chainsaw.json"""
    with open('chainsaw.json', 'r') as file:
        return json.load(file)


def add_subtree_to_json(subtree):
    """Attempts to add a given subtrees information to the chainsaw.json file"""
    chainsaw_json = load_json()
    chainsaw_json.append(subtree)
    json.dump('chainsaw.json', chainsaw_json)


def pull(args):
    pass


def add(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', dest='all', action='store_true', help='Add all subtrees defined in chainsaw.json')
    parser.add_argument('--squash', dest='squash', action='store_true', help='Squash subtree history into one commit')
    parser.add_argument('prefix', nargs='?', default=None, help='Specify subtree prefix (path from top level)')
    parser.add_argument('remote', nargs='?', default=None, help='Remote url of subtree')
    parser.add_argument('ref', nargs='?', default=None, help='Ref of subtree (ie. master)')
    args = parser.parse_args(args)

    if args.all:
        for subt in load_json():
            command = filter_none(['add', '-P', subt['prefix'], subt['remote'], subt['branch'], '--squash' if args.squash else None])
            subtree(*command)
    elif args.prefix and args.remote and args.ref:
        command = filter_none(['add', '-P', args.prefix, args.remote, args.ref, '--squash' if args.squash else None])
        subtree(*command)
    else:
        print(parser.parse_args(['--help']))


def push(args):
    pass


def revert(args):
    pass


def merge(args):
    pass


def unknown_action(args):
    print('Invalid command')


ACTIONS = {
    'pull': pull,
    'add': add,
    'push': push,
    'revert': revert,
    'merge': merge
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='Subtree Action: {}'.format(' '.join(ACTIONS.keys())))
    known, action_args = parser.parse_known_args()

    action = ACTIONS.get(known.action, unknown_action)

    action(action_args)


if __name__ == '__main__':
    main()
