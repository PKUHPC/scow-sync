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
            default='localhost',
            help='address of the server, default is localhost'
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
            default=2,
            help='max depth of the directory, default is 2'
        )

        # sshpassword-path
        self.parser.add_argument(
            '-p', '--sshpassword-path',
            type=str,
            default='~/.ssh/id_rsa',
            help='path of the ssh password file, default is ~/.ssh/id_rsa'
        )

        return self.parser
