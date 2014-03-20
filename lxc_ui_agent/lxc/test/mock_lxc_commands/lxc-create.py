import argparse

if __name__ == "__main__":  # pragma: nocover
    parser = argparse.ArgumentParser(description='Mock version of lxc-create.')
    parser.add_argument('--lxcpath', help='path where the lxc data is found')
    parser.add_argument('--name', help='name of the container')
    parser.add_argument('--template', help='template the container should be created from.')

    args = parser.parse_args()
    if args.lxcpath is None or args.name is None or args.template is None:
        parser.print_help()
        exit(1)

    # Actual implementation
    import os
    # do this funny import because we have a - in the name...
    lxc_stop = __import__('lxc-stop')
    # import time

    if args.template not in ["ubuntu", ]:
        print("lxc-create: bad template")
        exit(1)

    container_dir = os.path.join(args.lxcpath, args.name)
    try:
        os.makedirs(container_dir)
        print("created directory", container_dir)
        print("Many lines of stuff goes here\n" * 20)
        print("Login with ubuntu and ubuntu onto the container... bla bla... ssh keys... bla bla...")
        # time.sleep(10)

    except OSError as exc:
        print("Container already exists")
        exit(1)

    lxc_stop.write_stopped(container_dir)



