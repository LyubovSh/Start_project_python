#Калькулятор

#Ввод выражения осуществляется пользователем через консоль, будем запрашивать данные в формате str, затем преобразуем строку в массив, каждая ячейка которого хранит в себе число или арифметическую операцию
source_string = input('Введите арифметическое выражение, разделяя числа и операции пробелами').split()
print('Выражение в инфиниксной нотации', source_string)

#Преобразуем число к представлению в постфиксной форме записи(Обратная польсьская нотация). Операнды(числа) и операции будут предаставлять собой стеки.
def Reverse_Polish_notation(n):
    operations = []
    variables = []
    number_or_operation = '(+-*/^)' 
    current_element_priority, stack_element_priority = None, None 
    #Функция для опеределения приоритета арифметической операции
    def Get_priority(symbol):
        priority = 0
        if symbol == '*' or symbol == '/':
            priority = 3
        elif symbol == '+' or symbol == '-':
            priority = 2
        elif symbol == '(' or symbol == ')':  
            priority = 1    
        return priority
    
    for i in range(len(n)):
        #print('Текущий элемент', n[i])
        if n[i] not in number_or_operation:
            variables.append(float(n[i]))
        # Обрабатываем унарный минус    
        elif n[i] == '-' and (i == 0 or n[i - 1] in number_or_operation + '('):   
            variables.append(float(n[i + 1]) * -1)
            n[i + 1] = '0'
        elif n[i] in number_or_operation:
            #Определим приоритет тех операций, с которыми мы работаем, с помощью функции, описанной ниже
            current_element_priority = Get_priority(n[i])
            #Из вершины стека необходимо получить первый элемент и также определить его приоритет 
            if operations:
                stack_element_priority = Get_priority(operations[-1])
            #Теперь сравним приоритеты текущего элемента и элемента в стеке: Если приоритет текущей операции <= приоритета первой операции в стеке: Взять последнее число из стека operations и поместить в стек variables
                if (current_element_priority) <= (stack_element_priority):
                    tmp = operations.pop()
                    variables.append(tmp)
                    operations.append(n[i])
                else:
                    operations.append(n[i])
            #Если это первый элемент в нашем стеке
            else:
                tmp = n[i]
                operations.append(tmp)
        #print('Наши списки после одного шага цикла', variables, operations)    
                
    variables.extend(operations[::-1])   #Объединяем стеки        
    return variables

print('Выражение в постфиксной нотации', Reverse_Polish_notation(source_string))

#Сохраняем представление арифметического выражения в постфиксной нотации
postfix_representation = (Reverse_Polish_notation(source_string))     

#Теперь для дальнейшего вычисления выражения определим арифметические операции
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
        # Проверяем текущий символ в стеке является операндом или оператором 
        #Если операнд:
        if isinstance(token, float): 
            stack.append(token)
        #Если оператор    
        else:  
            b = stack.pop()
            a = stack.pop()
            stack.append(calc(a, b, token))    
    return stack

result = to_calculate(postfix_representation)

print('Ответ:', *result)