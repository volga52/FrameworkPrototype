import quopri


def decode_value(data):
    '''Функция декодирует значения словаря'''
    new_data = {}
    for k, v in data.items():
        val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val).decode('UTF-8')
        new_data[k] = val_decode_str
    return new_data
