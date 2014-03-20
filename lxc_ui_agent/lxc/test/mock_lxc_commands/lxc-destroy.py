import argparse

parser = argparse.ArgumentParser(description='Mock version of lxc-destroy.')
parser.add_argument('--lxcpath', help='path where the lxc data is found')
parser.add_argument('--name', help='name of the container')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.lxcpath is None or args.name is None:
        parser.print_help()
        exit(1)

    # Actual implementation
    import os
    import shutil

    container_dir = os.path.join(args.lxcpath, args.name)
    if not os.path.isdir(container_dir):
        print("Container is not defined")
        exit(1)

    try:
        shutil.rmtree(container_dir)
    except:
        print("Container is not defined")
        exit(1)





