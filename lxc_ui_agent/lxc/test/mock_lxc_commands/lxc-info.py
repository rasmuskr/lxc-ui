import argparse

parser = argparse.ArgumentParser(description='Mock version of lxc-info.')
parser.add_argument('--lxcpath', help='path where the lxc data is found')
parser.add_argument('--name', help='name of the container')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.lxcpath is None or args.name is None:
        parser.print_help()
        exit(1)

    # Actual implementation
    import os

    container_dir = os.path.join(args.lxcpath, args.name)
    if not os.path.isdir(container_dir):
        print("Container is not defined")
        exit(1)

    info_file = os.path.join(container_dir, "info_file")
    with open(info_file, "r") as f:
        print f.read()





