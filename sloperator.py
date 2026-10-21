import sys
from pathlib import Path

from sloperator.runner import check_program, run_program

USAGE = "usage: uv run sloperator.py [--check] <file.slop>"


def main(argv: list[str]) -> int:
    args = argv[1:]
    check = "--check" in args
    paths = [arg for arg in args if arg != "--check"]
    if len(paths) != 1:
        print(USAGE, file=sys.stderr)
        return 2

    path = Path(paths[0])
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"could not read '{path}': {error.strerror}", file=sys.stderr)
        return 2

    if check:
        error = check_program(source)
    else:
        error = run_program(source, sys.stdout)
    if error is not None:
        sys.stdout.flush()
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
