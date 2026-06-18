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

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "query":
        from repodanta.commands.trace import run_trace
        run_query(args)
    elif args.command == "inspect":
        from repodanta.commands.inspect import run_inspect
        run_inspect(args)
    elif args.command == "trace":
        from repodanta.commands.query import run_query
        run_trace(args)