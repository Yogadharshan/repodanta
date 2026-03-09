from repodanta.commands.core import load_repo, load_index_and_chunks
from repodanta.query_engine import answer_query


def run_query(args):
    repo = load_repo(args.path)
    index, chunks, _ = load_index_and_chunks(repo, args.path)
    answer = answer_query(args.question, repo, index, chunks)
    print("\nanswer\n")
    print(answer)