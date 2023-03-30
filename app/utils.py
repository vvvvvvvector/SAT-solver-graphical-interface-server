def string_to_int(string_arr):
    int_arr = []

    for variable in string_arr[:-1]:
        if variable.startswith('+'):
            raise Exception("Variable can't start with '+'")

        int_arr.append(int(variable))

    return int_arr


def remove_duplicates(clauses):
    return list(dict.fromkeys(clauses))
