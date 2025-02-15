import re

# Ввод выражения пользователем
source_string = input('Введите арифметическое выражение (например, (a+b)*c): ')

# Проверка наличия недопустимых символов
if re.search(r'[^a-zA-Z0-9+\-*/().\s]', source_string):
    print('Ошибка: обнаружен недопустимый символ.')
elif source_string.count('(') != source_string.count(')'):
    print('Ошибка: неточность в расстановке скобок (количество открывающих и закрывающих скобок не совпадает).')
elif '()' in source_string or re.search(r'\(\s*\)', source_string):  # Проверка на пустые скобки
    print('Ошибка: найдены пустые скобки.')
elif re.search(r'\)\s*\(', source_string) or re.search(r'[a-zA-Z]\(', source_string) or re.search(r'\)[a-zA-Z]', source_string):
    print('Ошибка: отсутствует операция между скобками или переменной и скобками (например, (a+b)(c-d) или a(b+c)).')
elif re.search(r'[a-zA-Z]{2,}', source_string):  # Проверка на отсутствие операции между переменными
    print('Ошибка: отсутствует операция между переменными (например, ab вместо a*b).')
else:
    # Разделяем числа, переменные и операции, включая унарные минусы
    tokens = re.findall(r'[a-zA-Z]|\d+\.\d+|\d+|[+\-*/()]', source_string)
    print('Выражение в инфиксной нотации:', tokens)

    # Определяем переменные в выражении
    variables = sorted(set(token for token in tokens if token.isalpha()))

    # Запрашиваем значения переменных у пользователя
    values = {}
    for var in variables:
        values[var] = float(input(f'Введите значение {var}: '))

    # Функция преобразования в постфиксную нотацию (ОПН)
    def Reverse_Polish_notation(n):
        operations = []
        output = []
        number_or_operation = '(+-*/)'

        # Функция для определения приоритета арифметической операции
        def Get_priority(symbol):
            priority = 0
            if symbol in ('*', '/'):
                priority = 3
            elif symbol in ('+', '-'):
                priority = 2
            elif symbol == '(':
                priority = 1
            return priority

        i = 0
        while i < len(n):
            if n[i].isalpha():  # Если переменная
                output.append(n[i])
            elif n[i].isdigit() or ('.' in n[i] and n[i].replace('.', '').isdigit()):  # Если число
                output.append(float(n[i]))
            elif n[i] == '-' and (i == 0 or n[i - 1] in number_or_operation + '('):
                output.append(float(n[i + 1]) * -1)
                i += 1  # Пропускаем следующий элемент, так как он уже обработан
            elif n[i] == '(':
                operations.append(n[i])
            elif n[i] == ')':
                while operations and operations[-1] != '(':
                    output.append(operations.pop())
                operations.pop()
            elif n[i] in number_or_operation:
                while operations and operations[-1] != '(' and Get_priority(n[i]) <= Get_priority(operations[-1]):
                    output.append(operations.pop())
                operations.append(n[i])
            i += 1

        # Объединяем стеки
        while operations:
            output.append(operations.pop())

        return output

    postfix_representation = Reverse_Polish_notation(tokens)
    print('Выражение в постфиксной нотации:', postfix_representation)

    # Функция для вычисления результата по постфиксной записи
    def calc(a, b, symbol):
        if symbol == '+':
            return a + b
        elif symbol == '-':
            return a - b
        elif symbol == '*':
            return a * b
        elif symbol == '/':
            if b == 0:
                raise ZeroDivisionError
            return a / b

    # Вычисляем результат по постфиксной нотации
    def to_calculate(postfix_representation, values):
        stack = []
        contains_operations = False  # Флаг, проверяющий, была ли выполнена арифметическая операция

        for token in postfix_representation:
            if isinstance(token, float):
                stack.append(token)
            elif token.isalpha():  # Если переменная, заменяем её на значение
                stack.append(values[token])
            else:
                contains_operations = True
                b = stack.pop()
                a = stack.pop()
                try:
                    stack.append(calc(a, b, token))
                except ZeroDivisionError:
                    print('Ошибка: попытка деления на ноль.')
                    return None, False

        return stack, contains_operations

    result, contains_operations = to_calculate(postfix_representation, values)

    # Вывод результата с проверкой наличия арифметических операций
    if result is not None:
        if contains_operations:
            print('Ответ:', *result)
        else:
            print('Никаких арифметических операций не выполнено.')
