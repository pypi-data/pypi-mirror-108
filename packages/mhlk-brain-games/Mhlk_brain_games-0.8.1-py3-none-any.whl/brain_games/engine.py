import prompt


def start(game):
    QUANTITY_ROUND = 3
    start_round = 1
    print('Welcome to the Brain games!')
    name = prompt.string('May I have your name? ')
    print(f'Hello, {name}!')
    print(game.DESCRIPTION + '\n')
    while start_round <= QUANTITY_ROUND:
        result, question, = game.get_question()
        print('Question: ' + question)
        answer = prompt.string('Your answer: ')
        if result == answer:
            print('Correct!')
            start_round += 1
        else:
            print(
                f'"{answer}" is wrong answer ;(. '
                f'Correct answer was "{result}". '
            )
            print(f'"Let\'s try again, {name}!"')
            return
    print(f'Congratulations, {name}!')
