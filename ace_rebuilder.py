

def add_spaces(previous, current):
    if not previous or previous in {" (", "("} or current in {",", ".", ")"} or current[0] == "'":
        return current
    return " " + current


def rebuild_ace(file_name):
    result = []
    with open(file_name, "r") as f:
        partial_line = []
        for line in f:
            line = line.split('\t')
            if len(line) < 10:          # reached blank line, so end of sentence
                result.append("".join(partial_line))
                partial_line = []

            else:                       # should process
                if len(partial_line) > 0:
                    partial_line.append(add_spaces(partial_line[-1], line[3]))
                else:
                    partial_line.append(add_spaces(None, line[3]))

    # removes begin and end of file lines
    return result[1:-1]


def process_ace_dataset():
    for file_name in ["AFP_ENG_20030418.0556"]:
        data = rebuild_ace(file_name)
        with open("result/" + file_name, 'w') as target:
            target.writelines('\n'.join(data))
