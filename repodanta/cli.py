import argparse
from repodanta.commands.inspect import run_inspect
from repodanta.commands.trace import run_trace
from repodanta.commands.query import run_query


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
        run_query(args)
    elif args.command == "inspect":
        run_inspect(args)
    elif args.command == "trace":
        run_trace(args)