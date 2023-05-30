import os
import re

from curtsies.fmtfuncs import red


def remove_comments(string):
    """Remove comments from a given string"""
    string = re.sub(re.compile("'''.*?'''", re.DOTALL), "", string)
    string = re.sub(re.compile('""".*?"""', re.DOTALL), "", string)
    string = re.sub(re.compile("#.*?\n"), "", string)

    return string


MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 256
NEWLINE_CHAR = "<N>"


def get_file_paths(root_dir):
    """Get a list of all file paths in a given directory and its subdirectories"""
    file_paths = []
    for dir_path, _, file_names in os.walk(root_dir):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            file_paths.append(file_path)
    return file_paths


def process_file(file_path, max_char_length, min_char_length, newline_char):
    """Process a given file and write its contents to a file if its length meets the specified criteria"""
    try:
        with open(file_path, "r") as file:
            contents = file.read()
    except:
        return
    contents = remove_comments(contents)
    contents = contents.replace("\n", newline_char)

    if 100 < len(contents) <= max_char_length:
        with open("data.txt", "a") as output_file:
            output_file.write(contents + '\n')
    elif len(contents) > max_char_length:
        sub_str = ""
        for split in contents.split(newline_char):
            sub_str += split + f"{newline_char}{newline_char}"
            if min_char_length <= len(sub_str) <= max_char_length:
                with open("data.txt", "a") as output_file:
                    output_file.write(sub_str + '\n')
                sub_str = ""
    else:
        print(red("Not enough length to consider"))


if __name__ == "__main__":
    root_dir = "repos"
    file_paths = get_file_paths(root_dir)
    for file_path in file_paths:
        process_file(file_path, MAX_CHAR_LENGTH, MIN_CHAR_LENGTH, NEWLINE_CHAR)
