"""Print a greeting."""
import argparse


def greet(name, shout=False):
    text = f"Hello, {name}!"
    return text.upper() if shout else text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--shout", action="store_true")
    args = parser.parse_args(argv)
    print(greet(args.name, args.shout))


if __name__ == "__main__":
    main()
