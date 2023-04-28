#! /usr/bin/env python3

import argparse
import json
import os
from pathlib import Path

import tomlkit


def list_ips(data: dict[str, str], _):
    for k, v in data.items():
        print(k, v)


def add_ip(data: dict[str, str], args):
    data[args.ip] = args.tag


def rm_ip(data: dict[str, str], args):
    if args.ip != "127.0.0.1" and not data.pop(args.ip, None):
        should_delete_ip = None
        for ip, tag in data.items():
            if tag == args.ip:
                should_delete_ip = ip
                break
        if should_delete_ip:
            data.pop(should_delete_ip, None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ip-allowlist")
    parser.add_argument(
        "--data",
        type=Path,
        default=os.environ.get("IP_ALLOWLIST_DATA_PATH"),
    )
    parser.add_argument(
        "--out",
        type=argparse.FileType("w"),
        default=os.environ.get("IP_ALLOWLIST_GENERATE_PATH"),
    )

    subparsers = parser.add_subparsers()

    parser_ls = subparsers.add_parser("ls")
    parser_ls.set_defaults(func=list_ips)

    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("ip", type=str)
    parser_add.add_argument("tag", type=str)
    parser_add.set_defaults(func=add_ip)

    parser_rm = subparsers.add_parser("rm")
    parser_rm.add_argument("ip", type=str)
    parser_rm.set_defaults(func=rm_ip)

    args = parser.parse_args()
    data = {}
    with open(args.data, "r") as f:
        data.update(json.load(f))

    args.func(data, args)

    doc = tomlkit.document()
    doc.add(tomlkit.comment("AUTO GENERATED FILE. DO NOT EDIT"))
    doc.add(tomlkit.nl())

    ip_source = tomlkit.table()
    ip_source["sourceRange"] = list(data.keys())

    ip_allowlist = tomlkit.table()
    ip_allowlist["ipAllowList"] = ip_source

    middlewares = tomlkit.table()
    middlewares["ip-allowlist"] = ip_allowlist

    http = tomlkit.table()
    http["middlewares"] = middlewares

    doc["http"] = http
    tomlkit.dump(doc, args.out)

    with open(args.data, "w") as f:
        json.dump(data, f)
