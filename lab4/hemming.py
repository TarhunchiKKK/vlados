import random

fcs_length: int = 5 # длина fcs (по твоему варику на такая)


# в коде часто встречается перевод строки в список
# это делается потому, что в строке нельзя уудалить или вставить символ в конкретной позиции,
# а в списке можно

# искажение случайного бита с вероятностью 70 проц
def distort_data(data: str) -> str:
    if random.random() <= 0.7:
        # получаем случайный бит
        distorted_bit_index: int = random.randint(0, 17)
        # перевод строки в список и искажение случайного бита
        data_list: list[str] = list(data)
        if data_list[distorted_bit_index] == '0':
            data_list[distorted_bit_index] = '1'
        else:
            data_list[distorted_bit_index] = '0'
        return list_to_str(data_list)
    # иначе возвращаем то, что было
    return data


#  перевод списка символов в строку
def list_to_str(lst: list[str]) -> str:
    data: str = ""
    for i in lst:
        data += i
    return data

# код хэмминга
def code(data: str) -> str:
    # в эти позиции будут вставляться контрольные биты
    control_positions: list[int] = [1,2,4,8,16]
    # сюда будет записывться fcs
    fcs: str = ''

    # символ в начало добавляется для выравнивания индексов
    # (в коде хэмминга индексация с 1, а в строке с 0)
    data = '$' + data
    data_list: list[str] = list(data)
    # вставляем контрольные биты
    for position in control_positions:
        data_list.insert(position, '1')

    # список значений контрольных битов
    values: list[str] = []

    # значения контрольных битов
    first_control_bit: str = data_list[1] + data_list[3] + data_list[5] + data_list[7] + data_list[9] + data_list[11] + \
                             data_list[13] + data_list[15] + data_list[17] + data_list[19] + data_list[21] + data_list[23]
    second_control_bit: str = data_list[2] + data_list[3] + data_list[6] + data_list[7] + data_list[10] + data_list[11] + \
                             data_list[14] + data_list[15] + data_list[18] + data_list[19] + data_list[22] + data_list[23]
    third_control_bit: str = data_list[4] + data_list[5] + data_list[6] + data_list[7] + data_list[12] + data_list[13] + \
                             data_list[14] + data_list[15] + data_list[20] + data_list[21] + data_list[22] + data_list[23]
    fourth_control_bit: str = data_list[8] + data_list[9] + data_list[10] + data_list[11] + data_list[12] + data_list[13] + \
                             data_list[14] + data_list[15]
    fifth_control_bit: str = data_list[16] + data_list[17] + data_list[18] + data_list[19] + data_list[20] + data_list[21] + \
                             data_list[22] + data_list[23]

    # добавление значений в список
    values.append(first_control_bit)
    values.append(second_control_bit)
    values.append(third_control_bit)
    values.append(fourth_control_bit)
    values.append(fifth_control_bit)

    # вычисление контрольных битов
    # (четное кол-во единиц - 0, иначе 1)
    for value in values:
        if value.count('1') % 2 == 0:
            fcs += '0'
        else:
            fcs += '1'

    return fcs

# исправление ошибки
def fix_data(data: str, fcs: str) -> str:
    # в эти позиции будут вставляться контрольные биты
    control_positions: list[int] = [1, 2, 4, 8, 16]

    # пересчет fcs на стороне приемника
    calculated_fcs: str = code(data)
    # позиции несовпадающих контрольных битов
    incorrect_bits_positions: list[int] = []
    # добавление позиций несовпадающих битов fcs
    for i in range (0, fcs_length):
        if fcs[i] != calculated_fcs[i]:
            incorrect_bits_positions.append(control_positions[i])

    # позиция неверного бита == сумма позиций несовпадающих контрольных битов
    incorrect_bit: int = 0
    for bit_position in incorrect_bits_positions:
        incorrect_bit += bit_position

    # символ добавляется для выравнвания индексов
    data = '$' + data
    data_list: list[str] = list(data)
    # вставка контролных битов в список
    for position in control_positions:
        data_list.insert(position, '1')

    # изменяем значение контрольного бита на противоположное
    if data_list[incorrect_bit] == '0':
        data_list[incorrect_bit] = '1'
    else:
        data_list[incorrect_bit] = '0'

    # контрольные биты удаляются в обратном порядке
    # иначе поплывуьт индексы
    control_positions.reverse()
    for i in control_positions:
        data_list[i] = ''

    # первый символ - доллар
    return list_to_str(data_list)[1::1]




print(fix_data('100010101010101010', '01010'))




