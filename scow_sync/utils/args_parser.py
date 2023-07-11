'''
Arguments parser 
'''
import argparse


def start_args_parse():
    '''
    parse command line arguments for scow-sync-start
    '''
    parser = argparse.ArgumentParser(
        description='argsparser for starting transferring files'
    )

    parser.add_argument(
        '-a', '--address',
        type=str,
        help='address of the server'
    )
    parser.add_argument(
        '-u', '--user',
        type=str,
        help='username for logging in'
    )
    parser.add_argument(
        '-s', '--source',
        type=str,
        help='path of the source file or directory'
    )
    parser.add_argument(
        '-d', '--destination',
        type=str,
        help='path of the destination directory'
    )
    parser.add_argument(
        '-m', '--max-depth',
        type=int,
        help='max parallel depth of the directory'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        help='ssh port of the server'
    )
    parser.add_argument(
        '-k', '--sshkey-path',
        type=str,
        help='path of the private key'
    )
    parser.add_argument(
        '-c', '--check',
        action='store_true',
        help='check whether the key in scow-sync-ssh is right'
    )

    args = parser.parse_args()
    return args

def terminate_args_parse():
    '''
    parse command line arguments for scow-sync-terminate
    '''
    parser = argparse.ArgumentParser(
        description='argsparser for terminating transferring files'
    )

    parser.add_argument(
        '-a', '--address',
        type=str,
        help='address of the server'
    )
    parser.add_argument(
        '-u', '--user',
        type=str,
        help='username for logging in to the server'
    )
    parser.add_argument(
        '-s', '--source',
        type=str,
        help='path to the source file or directory'
    )

    args = parser.parse_args()
    return args
