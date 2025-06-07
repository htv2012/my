#!/usr/bin/env python3
"""
Set the password for a user from a remote NGINX Controller.

Due to the restriction from the remote host, the remote user must
use sudo to read from and write to a file. There is no password for
sudo.

This script performs the following:

1. Read the contents of the htpasswd file (via sudo cat)
2. Remove the specified user's entry
3. Call openssl from the remote host to create a new password entry
4. Update the content
5. Upload that content to the remote host (via sudo cat)
6. Show the contents of the updated file, user can use the -q flag to suppress this
"""
#whatis: Supports the adm-passwd command
import argparse
import contextlib
import json
import os
import pathlib
import shlex

import paramiko


def main():
    parser = argparse.ArgumentParser(prog="adm passwd")
    parser.add_argument("username")
    parser.add_argument("password", nargs="?")
    parser.add_argument("-q", "--quiet", default=False, action="store_true")
    options = parser.parse_args()

    # Read the symbols
    symbols_file = os.getenv("TESTRUN_SYMBOLS") or os.getenv("SYSTEST_SYMBOLS")
    symbols_file = pathlib.Path(symbols_file)
    assert symbols_file.exists(), \
        "Please define environment variable TESTRUN_SYMBOLS or SYSTEST_SYMBOLS"
    with open(symbols_file, encoding="utf-8") as stream:
        symbols = json.load(stream)

    # Determine the private key file
    private_key_path = pathlib.Path(symbols_file).with_name("id_ed25519_testenv")
    assert private_key_path.exists(), f"{private_key_path} not found"
    private_key_path = str(private_key_path)

    with contextlib.ExitStack() as exit_stack:
        # Create a ssh connection to the controller
        client = exit_stack.enter_context(paramiko.SSHClient())
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(
            hostname=symbols["control_host_ips"][0],
            username=symbols["control_host_ssh_username"],
            key_filename=private_key_path,
        )

        # 1. Read the contents of the htpasswd file (via sudo cat)
        htpasswd_path = "/etc/nms/nginx/.htpasswd"
        _, stdout, _ = client.exec_command(f"sudo cat {htpasswd_path}")

        # 2. Remove the specified user's entry
        username = options.username
        lines = [line for line in stdout if not line.startswith(username)]

        # 3. Call openssl from the remote host to create a new password entry
        password = options.password or "Testenv12$"
        command = shlex.join(["sudo", "openssl", "passwd", "-6", password])
        _, stdout, _ = client.exec_command(command)
        # hashed included the trailing newline, which is OK
        hashed = stdout.read().decode()

        # 4. Update the content
        lines.append(f"{username}:{hashed}")
        lines = [line if line.endswith("\n") else f"{line}\n" for line in lines]

        # 5. Upload that content to the remote host
        remote_temp_path = "/tmp/temp-htpasswd"
        with client.open_sftp() as sftp, sftp.file(remote_temp_path, "wb") as stream:
            stream.writelines(lines)
        client.exec_command(f"sudo cp {remote_temp_path} {htpasswd_path}")
        client.exec_command(f"rm -f {remote_temp_path}")

        # 6. Show the contents after updated
        if not options.quiet:
            _, stdout, _ = client.exec_command(f"sudo cat {htpasswd_path}")
            contents = stdout.read().decode()
            print(f"--- {htpasswd_path} ---")
            print(contents)
            print("-----------------------")


if __name__ == "__main__":
    main()
