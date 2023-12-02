flag: str = '00010010'          # исходный флаг
new_flag: str = '00010011'      # флаг после бит стаффинга
data_len: int = 18              # длина твоей даты по варианту


# добавление data символом $, если введено меньше 18 символов
def complete_data(data: str) -> str:
    return data + (data_len - len(data)) * '$'

# получение source address (номер порта в бинарном виде)
def get_source_address(port_name: str) -> str:
    port_number: int = int(port_name[-1::1])
    binary_port_number: str = ''
    while port_number > 0:
        binary_port_number = str(port_number % 2) + binary_port_number
        port_number //= 2
    port_number_length: int = len(binary_port_number)
    return (4 - port_number_length) * '0' + binary_port_number

# бит стаффинг (замена всех вхождений flag на new_flag)
# суть в том, что мы находим по одному вхождение flag в строку
# и меняем его на new_flag
def bit_staffing(data: str) -> str:
    # строка после бит-стаффинга
    staffed_data: str = ''
    # индекс, от которого начинаем искать очередной flag
    old_index: int = 8
    # ищем flag
    while(True):
        # ищем позицию вхождения очередного flag начиная с индекса old_index
        new_index = data.find(flag, old_index)
        # если флаг не найден - заканчиваем
        if new_index == -1:
            break
        # добавить кусок строки до очередного флага
        staffed_data += data[old_index:new_index:1]
        # добавить new_flag вместо flag
        staffed_data += new_flag
        # пропускаем 8 для того чтобы пропустить найденный флаг, иначе рискуем снова на него напороться
        old_index = new_index + 8
    return staffed_data

# дебитстаффинг (замена всех вхождений new_flag на flag)
# алгоритм полностью аналогичен бит-стаффингу (только не flag меняем на nw_flag, а наоборот)
def de_bit_staffing(data: str) -> str:
    destaffed_data: str = ''
    old_index: int = 8
    while (True):
        new_index = data.find(new_flag, old_index)
        if new_index == -1:
            break
        destaffed_data += data[old_index:new_index:1]
        destaffed_data += flag
        old_index = new_index + 8
    return destaffed_data


# выделение битов, полученных при битстаффинге
# (биты, полученные при битстаффинге, будут заносится в фигурные скобки)
def get_highlighted_data(data: str) -> str:
    # таким будет "выделенный" флаг
    highlighted_flag: str = '0001001{1}'
    # заменяем все вхождения new_flag на highlighted_flag
    return data[0:8:1] + data[8::1].replace(new_flag, highlighted_flag)

# введенную пользователем дату нужно разбить на строки длиннойй 18 (по условию у тебя n=18)
# суть алгоритма в том, что м будем делить data на интервалы по 18 символов
# если остается строка длинной меньше 18 - дополняем ее символом доллара
def split_input_data_on_cadres(data: str) -> list[str]:
    # массив строк, который будет получен
    cadres: list[str] = []
    # индекс начала разбиения
    index: int = 0
    while True:
        # оставшаяся строка короче 8 символов - дополняем ее и заканчиваем
        if index + data_len >= len(data):
            cadres.append(complete_data(data[index::1]))
            break
        # извлекаем подстроку длиной 18 символов начиная с позиции index
        cadres.append(data[index:index + data_len:1])
        # увеличиваем index для перехода к следующей извлекаемой строке
        index += data_len
    return cadres

# ты принимаешь данные в виде 1 строки (там может быть несколько кодров)
# нужно разбить на кадры
# этот алгоритм я под чистую у себя скопипастил (въебло было разбираться как он работает, но его алгоритм похож на предыдущие)
def split_recieved_data_on_cadres(data: str) -> list[str]:
    cadres: list[str] = []
    old_index: int = 0
    while True:
        flag_position: int = data.find(flag, old_index)
        if flag_position == -1:
            break
        old_index = flag_position
        new_index: int = data.find(flag, old_index + 16)
        if new_index == -1:
            cadres.append(data[old_index::1])
            break

        # этот if возможно вообще не нужен
        if new_index >= len(data):
            break

        cadres.append(data[old_index:new_index:1])

        old_index = new_index
    return cadres
