import argparse


def run():
    parser = argparse.ArgumentParser(
        prog="repodanta",
        description="repodanta — repository intelligence engine"
    )
    sub = parser.add_subparsers(dest="command")

    q = sub.add_parser("query")
    q.add_argument("path")
    q.add_argument("question")

    i = sub.add_parser("inspect")
    i.add_argument("path")

    t = sub.add_parser("trace")
    t.add_argument("path")
    t.add_argument("function")

    sub.add_parser("version")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "version":
        try:
            from importlib.metadata import version
            print(version("repodanta"))
        except Exception:
            print("0.1.0")
        return

    if args.command == "query":
        from repodanta.commands.query import run_query
        run_query(args)
    elif args.command == "inspect":
        from repodanta.commands.inspect import run_inspect
        run_inspect(args)
    elif args.command == "trace":
        from repodanta.commands.trace import run_trace
        run_trace(args)
