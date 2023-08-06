from random import randint


DESCRIPTION = 'Find the greatest common divisor of given numbers.'


def get_question():
    num1 = randint(1, 100)
    num2 = randint(1, 100)
    question = f"{str(num1)} {str(num2)}"
    return str(gcd(num1, num2)), question


def gcd(num1, num2):
    while num1 != num2:
        if num1 > num2:
            num1 = num1 - num2
        else:
            num2 = num2 - num1
    return str(num1)
