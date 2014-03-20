import argparse


if __name__ == "__main__":  # pragma: nocover
    parser = argparse.ArgumentParser(description='Mock version of lxc-ls.')
    parser.add_argument('--lxcpath', dest='lxcpath', help='path where the lxc data is found')
    args = parser.parse_args()
    if args.lxcpath is None:
        parser.print_help()
        exit(1)

    # Actual implementation
    import os

    if not os.path.exists(args.lxcpath):
        # it is okay for the path not to exists, that just means that there is no containers
        exit(0)

    for path in os.listdir(args.lxcpath):
        print(path)
