from random import randint, choice

DESCRIPTION = 'What is the result of the expression?'


def get_question():
    num_operator = choice('-+*')
    f_num = randint(1, 99)
    s_num = randint(1, 99)
    if num_operator == '-':
        result = f_num - s_num
    elif num_operator == '+':
        result = f_num + s_num
    elif num_operator == '*':
        result = f_num * s_num
    question = f'{str(f_num)} {num_operator} {str(s_num)}'
    return str(result), question
