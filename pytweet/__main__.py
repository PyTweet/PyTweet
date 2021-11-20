import argparse
import platform
import sys

import requests

import pytweet


def show_version():
    entries = []

    entries.append("- Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(sys.version_info))
    entries.append("- pytweet v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(pytweet.version_info))
    entries.append(f"- requests v{requests.__version__}")
    uname = platform.uname()
    entries.append("- system info: {0.system} {0.release} {0.version}".format(uname))
    print("\n".join(entries))


def core(args):
    if args.version:
        show_version()
    else:
        print(
            "Hi Thank you for using pytweet! You can do can do `python3 -m pytweet --version` for version info!\n\nDocs: https://py-tweet.readthedocs.io/ \nGithub: https://github.com/PyTweet/PyTweet/"
        )


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-v", "--version", action="store_true", help="shows the library versioninfo")
    argparser.set_defaults(func=core)
    return argparser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
