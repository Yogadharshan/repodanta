from repodanta.commands.core import load_repo
from repodanta.call_tracer import trace_call_chain


def run_trace(args):
    repo = load_repo(args.path)
    chain = trace_call_chain(repo, args.function)

    if not chain:
        print(f"\nno calls found for function: {args.function}\n")
        return

    print("\ncall chain\n")
    print("-" * 40)
    for module, function in chain:
        print(f"{module}:{function}")
    print("-" * 40)