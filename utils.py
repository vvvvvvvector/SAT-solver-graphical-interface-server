def string_to_int(string_arr):
    int_arr = []

    for variable in string_arr[:-1]:
        if variable.startswith('+'):
            raise Exception("Variable can't start with '+'")

        int_arr.append(int(variable))

    return int_arr


def remove_duplicates(clauses):
    return list(dict.fromkeys(clauses))


def compare_formulas(first, second):
    if len(first) != len(second):
        return False

    length = len(first)

    for i in range(length):
        line_in_first = list(filter(None, first[i].split(' ')))
        line_in_second = list(filter(None, second[i].split(' ')))

        if len(line_in_first) != len(line_in_second):
            return False

        for j in range(len(line_in_first)):
            if line_in_first[j] != line_in_second[j]:
                return False

    return True
