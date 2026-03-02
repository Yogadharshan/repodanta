import argparse
from pathlib import Path
from index_service import index_repo as index_repo
from output import print_stats as print_stats


parser = argparse.ArgumentParser(description="repodanta: a code search and generation tool")

#arguements for cli
parser.add_argument("index", type=str, help="path to the project directory")
parser.add_argument("analyze", type=str, help="analyze the codebase and build the index")
parser.add_argument("inspect", type=str, help="inspect the codebase and visualize dependencies")
parser.add_argument("duplicates", type=str, help="find duplicate code in the codebase")
parser.add_argument("improve", type=str, help="improve the codebase by suggesting refactorings and optimizations")

path = parser.parse_args().index
repo = index_repo(path)