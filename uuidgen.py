#!/usr/bin/env python3
import argparse
import sys
import uuid

def cmd_gen(args):
    version = args.version
    count = args.count
    for _ in range(count):
        if version == 1:
            print(uuid.uuid1())
        elif version == 4:
            print(uuid.uuid4())
        elif version == 5:
            import uuid as u
            ns = u.UUID(args.namespace) if args.namespace else u.NAMESPACE_DNS
            name = args.name or "example.com"
            print(u.uuid5(ns, name))
        elif version == 7:
            try:
                print(uuid.uuid7())
            except AttributeError:
                import os, struct, time
                ts = int(time.time() * 1000)
                rand = os.urandom(10)
                b = ts.to_bytes(6, "big") + rand
                b = bytearray(b)
                b[6] = (b[6] & 0x0f) | 0x70
                b[8] = (b[8] & 0x3f) | 0x80
                u = uuid.UUID(bytes=bytes(b))
                print(u)
        else:
            print(uuid.uuid4())

def cmd_parse(args):
    try:
        u = uuid.UUID(args.uuid)
    except ValueError:
        print("invalid UUID", file=sys.stderr)
        sys.exit(1)
    print(f"version: {u.version}")
    print(f"variant: {u.variant}")
    print(f"hex: {u.hex}")
    print(f"int: {u.int}")
    print(f"urn: {u.urn}")
    print(f"fields: {u.fields}")
    print(f"time (if v1/v7): {u.time if u.version in (1, 7) else 'N/A'}")

def cmd_validate(args):
    try:
        uuid.UUID(args.uuid)
        print("valid")
    except ValueError:
        print("invalid")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog="uuidgen", description="Generate and inspect UUIDs. Zero dependencies.")
    parser.add_argument("-v", "--version", type=int, choices=[1, 4, 5, 7], default=None, help="UUID version (shorthand for gen)")
    parser.add_argument("-n", "--count", type=int, default=None, help="number to generate (shorthand for gen)")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("gen", help="generate UUIDs")
    p_gen.add_argument("-v", "--version", type=int, choices=[1, 4, 5, 7], default=4, help="UUID version")
    p_gen.add_argument("-n", "--count", type=int, default=1, help="number to generate")
    p_gen.add_argument("--namespace", default=None, help="namespace for v5")
    p_gen.add_argument("--name", default=None, help="name for v5")
    p_gen.set_defaults(func=cmd_gen)

    p_parse = sub.add_parser("parse", help="parse a UUID")
    p_parse.add_argument("uuid", help="UUID to parse")
    p_parse.set_defaults(func=cmd_parse)

    p_val = sub.add_parser("validate", help="validate a UUID")
    p_val.add_argument("uuid", help="UUID to validate")
    p_val.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    if args.version is not None or args.count is not None:
        a = type("A", (), {})()
        a.version = args.version or 4
        a.count = args.count or 1
        a.namespace = None
        a.name = None
        cmd_gen(a)
        return
    if not args.command:
        a = type("A", (), {})()
        a.version = 4
        a.count = 1
        a.namespace = None
        a.name = None
        cmd_gen(a)
        return
    args.func(args)

if __name__ == "__main__":
    main()
