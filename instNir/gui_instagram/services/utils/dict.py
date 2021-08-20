import operator


#Useless
def sorted_dict(dict1: {}) -> {}:
    """Сортирует словарь в порядке убывания по значению value"""

    sorted_tuple = sorted(dict1.items(), key=operator.itemgetter(1))
    sorted_dict = {}

    for k, v in reversed(sorted_tuple):
        sorted_dict.update({k: v})

    return sorted_dict


#Useless
def get_short_dict(full_dict: {}, length: int) -> {}:
    """Возращает length первых элементов словаря"""

    short_dict = {}
    i = 0
    for key in full_dict.keys():
        if i >= length:
            break
        else:
            i += 1
        short_dict.update({key: full_dict[key]})

    return short_dict


#Useless
def merge_dict(dict1: {}, dict2: {}) -> {}:
    """Объединяет два словаря"""

    for key in dict2.keys():
        if dict1.get(key):
            dict1.update({key: dict1.get(key) + dict2.get(key)})
        else:
            dict1.update({key: dict2.get(key)})
    return dict1


def convert_dict_to_plot_array(dict_: {}) -> [[str, int]]:
    """Конвертирует словарь в вид, необходимый для постройки графика"""

    return [[key, dict_.get(key)] for key in dict_]
