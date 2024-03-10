from flask import Flask, render_template

"""
Root of the BingoSurvey application.
This is a creative way to take a survey or play a progressive game
over some period of time.

:author: Jackson Eshbaugh
:date: 03/10/2024
"""

app = Flask(__name__)

# Bingo Board consists of 5x5 grid of question objects (id and prompt and completed)
bingo_board = [
    {'id': 1, 'prompt': 'What is the capital of France?', 'completed': True},
    {'id': 2, 'prompt': 'What is the capital of Germany?', 'completed': False},
    {'id': 3, 'prompt': 'What is the capital of Italy?', 'completed': False},
    {'id': 4, 'prompt': 'What is the capital of Spain?', 'completed': False},
    {'id': 5, 'prompt': 'What is the capital of Portugal?', 'completed': False},
    {'id': 6, 'prompt': 'What is the capital of Belgium?', 'completed': False},
    {'id': 7, 'prompt': 'What is the capital of Netherlands?', 'completed': False},
    {'id': 8, 'prompt': 'What is the capital of Luxembourg?', 'completed': False},
    {'id': 9, 'prompt': 'What is the capital of Denmark?', 'completed': False},
    {'id': 10, 'prompt': 'What is the capital of Sweden?', 'completed': True},
    {'id': 11, 'prompt': 'What is the capital of Norway?', 'completed': False},
    {'id': 12, 'prompt': 'What is the capital of Finland?', 'completed': False},
    {'id': 13, 'prompt': 'What is the capital of Iceland?', 'completed': False},
    {'id': 14, 'prompt': 'What is the capital of Ireland?', 'completed': False},
    {'id': 15, 'prompt': 'What is the capital of United Kingdom?', 'completed': False},
    {'id': 16, 'prompt': 'What is the capital of Switzerland?', 'completed': False},
    {'id': 17, 'prompt': 'What is the capital of Austria?', 'completed': False},
    {'id': 18, 'prompt': 'What is the capital of Czech Republic?', 'completed': False},
    {'id': 19, 'prompt': 'What is the capital of Slovakia?', 'completed': False},
    {'id': 20, 'prompt': 'What is the capital of Hungary?', 'completed': False},
    {'id': 21, 'prompt': 'What is the capital of Poland?', 'completed': False},
    {'id': 22, 'prompt': 'What is the capital of Lithuania?', 'completed': False},
    {'id': 23, 'prompt': 'What is the capital of Latvia?', 'completed': False},
    {'id': 24, 'prompt': 'What is the capital of Estonia?', 'completed': False},
    {'id': 25, 'prompt': 'What is the capital of Russia?', 'completed': False}
]


@app.route('/board')
def bingo_board():
    """
    Renders the bingo board.

    :return: the rendered bingo board.
    """
    return render_template('board.html', title='Board', data=bingo_board)


if __name__ == '__main__':
    app.run()
