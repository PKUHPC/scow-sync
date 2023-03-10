'''
Parse command line arguments
'''
from argparse import ArgumentParser


class ArgsParser:
    '''
    Parse command line arguments
    '''

    def __init__(self):
        self.parser = ArgumentParser(
            description='file transfer system for SCOW'
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
            help='path of the sshkey file, default is'
        )

        # remove source files or not after transfer
        self.parser.add_argument(
            '-r', '--remove',
            type=int,
            help='remove source files or not after transfer(non-dir)'
        )

        return self.parser
