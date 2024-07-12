import os


def write_line_file(filename, line, mode="a"):
    # Ensure the directory exists, if there is one
    if "/" in filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Write the line to the file
    with open(filename, mode) as file:
        file.write(line + "\n")


def read_first_line_file(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as file:
        line = file.readline().strip()
        return line


def remove_first_line_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    with open(filename, "w") as file:
        file.writelines(lines[1:])
