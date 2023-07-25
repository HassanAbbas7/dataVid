import argparse
from convertBack import filify
from makeVideo import vidize

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My script description")
    parser.add_argument("--vidize", type=str, help="Give file name like --vidize sample.rar")
    parser.add_argument("--filify", type=bool, default=False, help="set true for converting a video like --filify true")

    args = parser.parse_args()
    if (args.vidize):
        print(args.vidize)
        vidize(args.vidize)
    elif args.filify:
        filify()
