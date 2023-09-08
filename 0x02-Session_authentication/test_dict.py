my_dict = {'a' : 1, 'b' : 2, 'c' : 3}


def valueKey(my_dict: dict, value: int) -> str :
    for key in my_dict.keys():
        if my_dict.get(key) == value:
            return key
    return keys

print(valueKey(my_dict, 3))