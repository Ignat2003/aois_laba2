import re


class BoolVar:
    def __init__(self, value):
        self.value = value

    # '-' — возражения "нет"
    def __neg__(self):
        return BoolVar(not self.value)

    # '+' — дизъюнкция "или"
    def __add__(self, other):
        return BoolVar(self.value or other.value)

    # '*' — конъюнкция "и"
    def __mul__(self, other):
        return BoolVar(self.value and other.value)

    # '>' — импликация "если ..., тогда"
    # def __gt__(self, other):
    #     return BoolVar(self.value <= other.value)

    # '=' — эквивалентность "ровно"
    def __eq__(self, other):
        return BoolVar(self.value == other.value)

    # строковое представление значения
    def __str__(self):
        return "True" if self.value else "False"

    def __format__(self, format_spec):
        return format(str(self), format_spec)


# infunc = input('Enter your function: ')
infunc = '((a=b)=c)'

infunc = infunc.replace("=", "==")
infunc = infunc.replace('>', '<=')
# находим переменные в функции, т.е. просто буквы
# set() делает этот набор уникальным, ну и сортируем
variables = sorted(set(re.findall(r"[A-Za-z]", infunc)))

# просто красивое оформление для таблицы
header = [""] * 2
for key in variables:
    header[0] += "-" * 7 + "+"
    header[1] += f"   {key}   |"
header[0] += "-+" + "-" * 7
header[1] += " | Result"
print("\n".join(header + header[0:1]))

vars_for_eval = {}
disjunctive_normal_form_safe = []
conjunctive_normal_form = []

# вариантов входных значений для таблицы - 2 в степени кол-ва переменных
for variant in range(1 << len(variables)):
    # заполняем входной словарь c представлением переменных
    # в виде экземпляров нашего класса для функции eval()
    # key идут в прямом порядке, а i - в обратном
    for i, key in reversed(list(enumerate(reversed(variables)))):
        # используем биты этого числа для инициализыции булевых значений
        vars_for_eval[key] = BoolVar(variant & (1 << i))
        # вывод строки таблицы истинности
        print(f" {vars_for_eval[key]:<5}", end=" |")
    # вычисляем результат
    func = infunc[:]
    for variable, is_true in vars_for_eval.items():
        is_true = str(bool(is_true.value))
        func = func.replace(variable, is_true)

    result = eval(func)

    if result:
        disjunctive_normal_form_safe.append(vars_for_eval.copy())
    else:
        conjunctive_normal_form.append(vars_for_eval.copy())

    print(f" | {result:<5}")
print(header[0])


print('Disjunctive_normal_form')
tmp_variable = ''

for form in disjunctive_normal_form_safe:
    for variable, is_true in form.items():
        print(' ' if is_true.value else '-',  end='')
        tmp_variable += variable
    print('   ', end='')
    tmp_variable += ' ∨ '
print()
print(''.join(tmp_variable[:-2]))


print('Conjunctive_normal_form')
tmp_variable = ''
for form in conjunctive_normal_form:
    tmp_variable += '('
    print(' ', end='')

    for variable, is_true in form.items():
        print('-' if is_true.value else ' ',  end='')
        tmp_variable += variable

    print('  ', end='')
    tmp_variable += ')∧'
print()
s = ''.join(tmp_variable[:-1])

print(s)
