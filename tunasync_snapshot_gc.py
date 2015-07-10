#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import re
import sh
import os
import argparse
import toml

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tunasync_snapshot_gc")
    parser.add_argument("--max-level", type=int, default=1, help="max walk level to find garbage snapshots")
    parser.add_argument("--pattern", default=r"^_gc_.+_\d+", help="pattern to match garbage snapshots")
    parser.add_argument("-c", "--config", help="tunasync config file")

    args = parser.parse_args()

    pattern = re.compile(args.pattern)

    def walk(_dir, level=1):
        if level > args.max_level:
            return

        for fname in os.listdir(_dir):
            abs_fname = os.path.join(_dir, fname)
            if os.path.isdir(abs_fname):
                if pattern.match(fname):
                    print("GC: {}".format(abs_fname))
                    try:
                        sh.btrfs("subvolume", "delete", abs_fname)
                    except sh.ErrorReturnCode, e:
                        print("Error: {}".format(e.stderr))
                else:
                    walk(abs_fname, level+1)

    with open(args.config) as f:
        settings = toml.loads(f.read())

    mirror_root = settings["global"]["mirror_root"]
    gc_root = settings["btrfs"]["gc_root"].format(mirror_root=mirror_root)

    walk(gc_root)

# vim: ts=4 sw=4 sts=4 expandtab
