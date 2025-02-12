str = input().split()
n, m = int(str[0]), int(str[1])
matrix = [[None] * m for _ in range(n)]
# У нас запись по строке сменяется записью по столбцу. Будем определять условное направление, создав своего рода флаг
mode = 'stolb'
if_str = n - 1  # То, сколько элементов мы должны пройти и изменить
if_stolb = m - 1

index_for_str = 0  # Прошли столбец? Сохраним индекс i последнего эл-а для след. строки
index_for_stolb = 0  # Прошли строку? Сохраним индекс j последнего эл-а для след. столбца
# Чтобы наши элементы заполнялись именно в той последовательности, в которой нам это нужно создадим переменную, сохраняющую сумму индексов элемента, удовлетворяющего условию. Таким образом, если сумма следующего элемента отличается на 1, то это необходимый нам элемент
summa = 0

tmp_for_elem = 1
tmp_for_direction = 0

while tmp_for_elem < (n * m)+1:
    # print(tmp_for_elem)
    for i in range(n):
        for j in range(m):

            #print('Индексы:', i, 'и', j, 'Режим и остаток по строке или столбцу', mode, if_str, if_stolb, index_for_stolb)
            if i == 0 and matrix[i][j] == None:
                matrix[i][j] = tmp_for_elem
                tmp_for_elem += 1
                summa = i + j
                index_for_stolb = m - 1
                #print('Я захожу')
            # Если идем по столбцу
            if mode == 'stolb' and abs((i + j) - summa) == 1 and index_for_stolb == j and matrix[i][j] == None:
                #print('Для столбца', 'Индексы:', i, 'и', j, matrix[i][j])
                matrix[i][j] = tmp_for_elem
                tmp_for_elem += 1
                summa = i + j
                tmp_for_direction += 1
                if tmp_for_direction == if_str:  # Изменили столько элементов, что текщий столбец должен прерваться
                    if_str -= 1  # В след. раз изменим на 1 меньше, а сейчас меняем направление
                    tmp_for_direction = 0
                    mode = 'str'
                    index_for_str = i
            # Если идем по строке
            if mode == 'str' and abs((i + j) - summa) == 1 and index_for_str == i and matrix[i][j] == None:
                #print('Для строки', 'Индексы:', i, 'и', j, matrix[i][j])
                matrix[i][j] = tmp_for_elem
                tmp_for_elem += 1
                summa = i + j
                tmp_for_direction += 1
                if tmp_for_direction == if_stolb:  # Изменили столько элементов, что текщий столбец должен прерваться
                    if_stolb -= 1  # В след. раз изменим на 1 меньше, а сейчас меняем направление
                    tmp_for_direction = 0
                    mode = 'stolb'
                    index_for_stolb = j

for i in range(n):
    print()
    for j in range(m):
        print(matrix[i][j], end = ' ')