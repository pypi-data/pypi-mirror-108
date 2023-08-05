from pathlib import Path

from .template import template


def main():
    newfile = Path().cwd() / ".gitignore"
    data = [line for line in template.readlines()]

    with open(newfile, "w") as f:
        for l in data:
            f.write(l)
    print(".gitignore added")
