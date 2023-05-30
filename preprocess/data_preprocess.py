import os
import re

from curtsies.fmtfuncs import red


def remove_comments(string):
    string = re.sub(re.compile("\'\'\'.*?\'\'\'", re.DOTALL), "", string)
    string = re.sub(re.compile("\"\"\".*?\"\"\"", re.DOTALL), "", string)
    string = re.sub(re.compile("#.*?\n"), "", string)

    return string


MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 256

NEWLINE_CHAR = "<N>"

full_paths = []
for dir_path, dir_names, file_names in os.walk("repos"):
    for f in file_names:
        full_path = os.path.join(dir_path, f)
        full_paths.append(full_path)

with open("data.txt", "a") as df:
    for path in full_paths:
        try:
            file = open(path, "r").read()
        except:
            continue

        file = remove_comments(file)
        f = file.replace("\n", NEWLINE_CHAR)

        if 100 < len(file) <= MAX_CHAR_LENGTH:
            df.write(f + '\n')
        elif len(file) > MAX_CHAR_LENGTH:
            sd = f.split(f"{NEWLINE_CHAR}")
            sub_str = ""
            for split in sd:

                sub_str += split + f"{NEWLINE_CHAR}{NEWLINE_CHAR}"
                if MIN_CHAR_LENGTH <= len(sub_str) <= MAX_CHAR_LENGTH:
                    df.write(sub_str + '\n')
                    sub_str = ""
        else:
            print(red("Not enough length to consider"))
