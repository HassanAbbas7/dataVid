import argparse
from convertBack import filify
from makeVideo import vidize

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My script description")
    parser.add_argument("--vidize", type=str, help="Description of argument 1")
    parser.add_argument("--filify", type=bool, default=False, help="Description of argument 2")

    args = parser.parse_args()
    if (args.vidize):
        print(args.vidize)
        vidize(args.vidize)
    elif args.filify:
        filify()
