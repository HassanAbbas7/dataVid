import argparse
from convertBack import filify
from makeVideo import vidize

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My script description")
    parser.add_argument("action", choices=["vidize", "filify"], help="Action to perform (e.g., makevideo)")
    parser.add_argument("--file", type=str, help="Give file name like --vidize sample.rar")
    parser.add_argument("--makeinblocks", type=bool, default=False, help="Give file name like --vidize sample.rar")
    parser.add_argument("--isblockencoding", type=bool, default=False, help="set true for converting a video like --filify true")

    args = parser.parse_args()
    if (args.action == "vidize"):
        vidize(args.file, makeInBlocks=args.makeinblocks)
    elif (args.action == "filify"):
        filify(makeInBlocks=args.isblockencoding)