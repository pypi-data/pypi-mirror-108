from random import randint

DESCRIPTION = 'What number is missing in the progression?'


def get_question():
    length_of_progression = 15
    start_progression = randint(1, 100)
    answer = randint(0, length_of_progression - 1)
    resolution = randint(1, 30)
    index_of_num = 0
    question = ''
    while index_of_num < length_of_progression:
        if index_of_num == answer:
            question += '.. '
            index_of_num += 1
        else:
            question += f'{start_progression + resolution * index_of_num} '
            index_of_num += 1
    result = start_progression + resolution * answer
    return str(result), question.rstrip()
