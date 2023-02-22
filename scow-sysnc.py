from scowsync import ScowSync
from argsparser import ArgsParser

# ok for file transfer
if __name__ == '__main__':
    args = ArgsParser().get_args_parser().parse_args()
    scow = ScowSync(args.address, args.user, args.password, args.source, args.destination)
    scow.transfer_files()