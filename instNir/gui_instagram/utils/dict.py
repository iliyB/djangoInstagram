import operator


def sorted_dict(dict1: {}) -> {}:
    sorted_turple = sorted(dict1.items(), key=operator.itemgetter(1))
    sorted_dict = {}

    for k, v in reversed(sorted_turple):
        sorted_dict.update({k: v})

    return sorted_dict


def get_short_dict(full_dict: {}, length: int) -> {}:
    short_dict = {}
    i = 0
    for key in full_dict.keys():
        if i >= length:
            break
        else:
            i += 1
        short_dict.update({key: full_dict[key]})

    return short_dict


def merge_dict(dict1: {}, dict2: {}) -> {}:
    for key in dict2.keys():
        if dict1.get(key):
            dict1.update({key: dict1.get(key) + dict2.get(key)})
        else:
            dict1.update({key: dict2.get(key)})
    return dict1
