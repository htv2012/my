#!/usr/bin/env python3
import argparse
import json
import pathlib
import shlex
import shutil
import subprocess

from .restconf import pretty_json


def curl(url, user, password):
    command = [
        "curl",
        "--silent",
        "--insecure",
        "--header", 'Accept: application/yang-data+json',
        "--user", f"{user}:{password}",
        url,
    ]

    print(" ".join(shlex.quote(t) for t in command))

    process = subprocess.Popen(command, stdout=subprocess.PIPE, encoding="utf-8")
    stdout, _ = process.communicate()
    return stdout


def main(args=None):
    """ Entry """
    common_resources = [
        "f5-cluster:cluster",
        "f5-dag:dag-states",
        "f5-l2fdb:fdb",
        "f5-port-mappings:port-mappings",
        "f5-portgroup:portgroups",
        "f5-service-instances:service-instances",
        "f5-service-pod:service-pods",
        "f5-services:services",
        "f5-tenant-images:images",
        "f5-tenants:tenants",
        "f5-utils-file-transfer:file",
        "f5-vlan-listeners:vlan-listeners",
        "ietf-netconf-monitoring:netconf-state",
        "ietf-restconf-monitoring:restconf-state",
        "ietf-yang-library:modules-state",
        "openconfig-interfaces:interfaces",
        "openconfig-lacp:lacp",
        "openconfig-lldp:lldp",
        "openconfig-spanning-tree:stp",
        "openconfig-system:system",
        "openconfig-vlan:vlans",
        "SNMP-VIEW-BASED-ACM-MIB:SNMP-VIEW-BASED-ACM-MIB",
        "SNMPv2-MIB:SNMPv2-MIB",
        "tailf-aaa:aaa",
        "tailf-confd-monitoring:confd-state",
        "tailf-rollback:rollback-files",
    ]

    formatted_list_of_resources = "\n".join(f"  {scope}" for scope in common_resources)
    epilog = f"\ncommon list of resources:\n{formatted_list_of_resources}"

    # Use argparse.RawTextHelpFormatter to prevent line wrapping of help text, incuding the epilog
    parser = argparse.ArgumentParser(
        prog="rct get",
        description="A tool to make RESTCONF GET calls to specific resources",
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("dut_ip")
    parser.add_argument("resource")
    options = parser.parse_args(args)

    url = f"https://{options.dut_ip}:8888/restconf/data/{options.resource}"
    output = curl(url, "admin", "ess-pwe-f5site02")

    # The output contains a dict with single value, we are interest in
    # that value, not the whole dict
    output = json.loads(output)
    output = next(iter(output.values()))
    pretty_json(output)


if __name__ == '__main__':
    main()
