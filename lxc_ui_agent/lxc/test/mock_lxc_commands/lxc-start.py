import argparse

parser = argparse.ArgumentParser(description='Mock version of lxc-start.')
parser.add_argument('--lxcpath', help='path where the lxc data is found')
parser.add_argument('--name', help='name of the container')
parser.add_argument('--daemon', action='store_true', default=False, help='name of the container')

RUNNING_STRING = "state:   RUNNING"


def write_start(container_dir):
    import os

    info_file = os.path.join(container_dir, "info_file")
    with open(info_file, "w+") as f:
        f.write(RUNNING_STRING)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.lxcpath is None or args.name is None or args.daemon is None:
        parser.print_help()
        exit(1)

    # Actual implementation
    import os

    if args.daemon is False:
        print("This should only be called with daemon to not block!")
        exit(1)

    container_dir = os.path.join(args.lxcpath, args.name)
    if not os.path.isdir(container_dir):
        print("Container is not defined")
        exit(1)

    info_file = os.path.join(container_dir, "info_file")
    with open(info_file, "r") as f:
        read_data = f.read()
        if read_data == RUNNING_STRING:
            print("Container already running")
            exit(1)

    write_start(container_dir)



