import os
from curtsies.fmtfuncs import red, green, yellow

REPOS_DIR = "repos"


def is_python_file(path):
    """
    Checks if a given file path is a Python file based on the extension.
    """
    return os.path.splitext(path)[1] == ".py"


def main():
    for dir_path, dir_names, file_names in os.walk(REPOS_DIR):
        for file_name in file_names:
            full_path = os.path.join(dir_path, file_name)

            if is_python_file(full_path):
                print(green(f"Keeping {full_path}"))
            else:
                print(red(f"Deleting {full_path}"))

                try:
                    os.remove(full_path)
                except OSError:
                    print(yellow(f"Failed to delete {full_path}"))


if __name__ == "__main__":
    main()
