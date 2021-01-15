from flask import Flask, request, render_template, redirect, jsonify, session
from boggle import Boggle


app = Flask(__name__)
# will help with debugging
app.config['SECRET_KEY'] = 'yek700terces'

boggle_game = Boggle()


@app.route('/')
def show_board():
    '''Show the board'''
    board = boggle_game.make_board()  # get make_board def from class Boggle
    session['board'] = board  # add board to session to remember
    # get highscore from session and set default 0
    highscore = session.get("highscore", 0)
    # get num of plays from session and set default to 0
    nplays = session.get("nplays", 0)
    return render_template('index.html', board=board, highscore=highscore, nplays=nplays)


@app.route('/check-word')
def guess_submitted_word():
    '''Submit a word and check if it valid'''
    word = request.args['word']  # get the word input from form
    board = session["board"]  # get board from session
    # getting check word function from boggle.py
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    '''Receive score, update nplays, update high score if appropriate.'''

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1  # every next session up the count by 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
