'''
ArgsParser for scow-sync
'''
# argsparser/__init__.py

__all__ = ['StartArgsParser', 'TerminateArgsParser']

from argparse import ArgumentParser


class StartArgsParser:
    '''
    Parse command line arguments for scow-sync-start
    '''

    def __init__(self):
        self.parser = ArgumentParser(
            description='start file transfer system for SCOW'
        )

    def get_args_parser(self) -> ArgumentParser:
        '''
        Get the argument parser
        @return: the argument parser
        '''

        # address
        self.parser.add_argument(
            '-a', '--address',
            type=str,
            help='address of the server'
        )

        # user
        self.parser.add_argument(
            '-u', '--user',
            type=str,
            help='username for logging in to the server'
        )

        # source path
        self.parser.add_argument(
            '-s', '--source',
            type=str,
            help='path to the source file or directory'
        )

        # directory path
        self.parser.add_argument(
            '-d', '--destination',
            type=str,
            help='path to the destination directory'
        )

        # max-depth
        self.parser.add_argument(
            '-m', '--max-depth',
            type=int,
            help='max depth of the directory'
        )

        # ssh port
        self.parser.add_argument(
            '-p', '--port',
            type=int,
            help='ssh port of the server'
        )

        # sshpassword-path
        self.parser.add_argument(
            '-k', '--sshkey-path',
            type=str,
            help='path of the private key'
        )

        # check whether the key in scow-sync-ssh is right
        self.parser.add_argument(
            '-c', '--check',
            action='store_true',
            help='check whether the key in scow-sync-ssh is right'
        )

        return self.parser


class TerminateArgsParser:
    '''
    Parse command line arguments for scow-sync-terminate
    '''

    def __init__(self):
        self.parser = ArgumentParser(
            description='start file transfer system for SCOW'
        )

    def get_args_parser(self) -> ArgumentParser:
        '''
        Get the argument parser
        @return: the argument parser
        '''

        # address
        self.parser.add_argument(
            '-a', '--address',
            type=str,
            help='address of the server'
        )

        # user
        self.parser.add_argument(
            '-u', '--user',
            type=str,
            help='username for logging in to the server'
        )

        # source path
        self.parser.add_argument(
            '-s', '--source',
            type=str,
            help='path to the source file or directory'
        )

        # ssh port
        self.parser.add_argument(
            '-p', '--port',
            type=int,
            help='ssh port of the server'
        )

        # sshpassword-path
        self.parser.add_argument(
            '-k', '--sshkey-path',
            type=str,
            help='path of the private key'
        )

        return self.parser
