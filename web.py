from flask import render_template, request, Flask

app = Flask(__name__)

from chess_vis.shared import (
    format_square,
    random_square,
    parse_square,
    evaluate_list_answer,
    is_valid_knight_jump,
    is_light_square,
    knight_jumps,
    mutual_bishop_squares,
    random_different_square,
    random_different_bishop_square,
    IncorrectSyntax,
    GameState,
)

QUESTIONS = ["square_color", "knight_jumps", "bishop_transfers"]


def render_home(
    game_state=None,
    error=None,
):
    if game_state is None:
        square = random_square()
        game_state = GameState(
            question=QUESTIONS[0],
            square=square,
            different_square=random_different_square(square),
            different_bishop_square=random_different_bishop_square(square),
            wrong=None,
        )

    return render_template(
        "index.html",
        error=error,
        question=game_state.question,
        square=format_square(game_state.square),
        different_square=format_square(game_state.different_square),
        different_bishop_square=format_square(game_state.different_bishop_square),
        wrong=game_state.wrong,
    )


@app.route("/", methods=["GET"])
def home():
    return render_home()


def grade(game_state, guess):
    guess = guess.lower().strip()

    if game_state.question == "square_color":
        solution = "light" if is_light_square(game_state.square) else "dark"
        return guess == solution

    if game_state.question == "knight_jumps":
        solution = knight_jumps(game_state.square)
        syntax, correct, wrong, *_ = evaluate_list_answer(guess, solution)
        print("wrong", wrong)
        print("correct", correct)
        print(solution)
        if not syntax:
            raise IncorrectSyntax()

        return not wrong

    if game_state.question == "bishop_transfers":
        return (
            mutual_bishop_squares(
                game_state.square, game_state.different_bishop_square
            ),
        )


@app.route("/", methods=["POST"])
def check_user_guess():
    guess = request.form["guess"]
    game_state = GameState(
        square=parse_square(request.form["square"]),
        different_square=parse_square(request.form["different_square"]),
        different_bishop_square=parse_square(request.form["different_bishop_square"]),
        question=request.form["question"],
        wrong=None,
    )
    print(request.form)

    if not guess:
        return render_home(game_state, error="A required field is missing.")

    try:
        game_state.wrong = not grade(game_state, guess)
    except IncorrectSyntax:
        return render_home(game_state, error="Input was formatted incorrectly")

    if not game_state.wrong:
        next_question = QUESTIONS.index(game_state.question) + 1
        if next_question >= len(QUESTIONS):
            square = random_different_square(game_state.square)
            game_state.different_square = random_different_square(square)
            game_state.different_bishop_square = random_different_bishop_square(square)
            next_question = 0

        game_state.question = QUESTIONS[next_question]

    return render_home(game_state)
