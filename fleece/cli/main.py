import sys
import pkg_resources

commands = ['build', 'run', 'config', 'shell']


def print_help():
    print('Available sub-commands: {}.'.format(', '.join(commands)))
    print('Use "fleece <sub-command> --help" for usage.')


def main():
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    if sys.argv[1] in commands:
        # Check that the CLI dependencies are installed before executing the
        # command.
        deps = pkg_resources.get_distribution('fleece')._dep_map.get(
            'cli', [])
        for dep in deps:
            try:
                # PyYAML really messes this up.
                if dep.project_name == 'PyYAML':
                    __import__('yaml')
                else:
                    __import__(dep.project_name)
            except ImportError:
                print('Dependency "{}" is not installed. Did you run '
                      '"pip install fleece[cli]"?'.format(dep))
                sys.exit(1)

        # execute the command
        module = __import__('fleece.cli.' + sys.argv[1])
        module = getattr(module.cli, sys.argv[1])
        getattr(module, 'main')(sys.argv[2:])
    else:
        if sys.argv[1] not in ['--help', '-h']:
            print('"{}" is not an available fleece sub-command.'.format(
                sys.argv[1]))
        print_help()
