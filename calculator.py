#Калькулятор

# Ввод выражения осуществляется пользователем через консоль, будем запрашивать данные в формате str, 
# затем преобразуем строку в массив, каждая ячейка которого хранит в себе число или арифметическую операцию
source_string = input('Введите арифметическое выражение, разделяя числа и операции пробелами: ').split()
print('Выражение в инфиниксной нотации', source_string)

# Преобразуем число к представлению в постфиксной форме записи (Обратная польская нотация).
# Операнды (числа) и операции будут представлять собой стеки.
def Reverse_Polish_notation(n):
    operations = []
    variables = []
    number_or_operation = '(+-*/)' 
    current_element_priority, stack_element_priority = None, None 
    
    # Функция для определения приоритета арифметической операции
    def Get_priority(symbol):
        priority = 0
        if symbol == '*' or symbol == '/':
            priority = 3
        elif symbol == '+' or symbol == '-':
            priority = 2
        elif symbol == '(':
            priority = 1
        return priority
    
    for i in range(len(n)):
        if n[i] not in number_or_operation:
            variables.append(float(n[i]))
        # Обрабатываем унарный минус    
        elif n[i] == '-' and (i == 0 or n[i - 1] in number_or_operation + '('):   
            variables.append(float(n[i + 1]) * -1)
            n[i + 1] = '0'
        # Обрабатываем oткрывающую скобку (добавляем в стек)   
        elif n[i] == '(':
            operations.append(n[i]) 
        # Обрабатываем закрывающую скобку (берем из стека операции до '(' )
        elif n[i] == ')':  
            while operations and operations[-1] != '(':
                variables.append(operations.pop())
            operations.pop() 
        elif n[i] in number_or_operation:
            # Определим приоритет текущей операции
            current_element_priority = Get_priority(n[i])
            # Из вершины стека получаем первый элемент и определяем его приоритет
            while operations and operations[-1] != '(' and current_element_priority <= Get_priority(operations[-1]):
                variables.append(operations.pop())
            operations.append(n[i])

    variables.extend(operations[::-1])   # Объединяем стеки        
    return variables

print('Выражение в постфиксной нотации', Reverse_Polish_notation(source_string))

# Сохраняем представление арифметического выражения в постфиксной нотации
postfix_representation = Reverse_Polish_notation(source_string)

# Теперь для дальнейшего вычисления выражения определим арифметические операции
def calc(a, b, symbol):
    if symbol == '+':
        return float(a) + float(b)
    elif symbol == '-':
        return float(a) - float(b)
    elif symbol == '*':
        return float(a) * float(b)
    elif symbol == '/':
        return float(a) / float(b)

# Из выражения, представленного в постфиксном представлении будем извлекать операнды и операторы, применяя функцию для вычисления арифметических операций. Если текущий символ число-оправляем его в стек, если арифметическая операция-выполняем её с помощью функции calc, извлекая числа из стека
def to_calculate(postfix_representation):
    stack = []    
    for token in postfix_representation:
        # Проверяем, является ли текущий символ в стеке операндом или оператором 
        # Если операнд:
        if isinstance(token, float): 
            stack.append(token)
        # Если оператор: 
        else:  
            b = stack.pop()
            a = stack.pop()
            stack.append(calc(a, b, token))    
    return stack

result = to_calculate(postfix_representation)

print('Ответ:', *result)
