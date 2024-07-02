from dataclasses import dataclass

from random import randint
import re


class GameEndException(Exception):
    pass


class IncorrectSyntax(Exception):
    pass


@dataclass
class GameState:
    question: str
    square: tuple[int, int]
    different_square: tuple[int, int]
    different_bishop_square: tuple[int, int]
    wrong: bool | None


def filter_illegal_squares(squares):
    filtered = []
    for s in squares:
        if 1 <= s[0] <= 8 and 1 <= s[1] <= 8:
            filtered.append(s)
    return filtered


def is_light_square(s):
    return (s[0] + s[1]) % 2 == 1


def random_square():
    return (randint(1, 8), randint(1, 8))


def square2int(s):
    line = (s[0] - 1) * 8
    rank = s[1] - 1
    # reverse rank, so even numbers are dark squares
    if s[0] % 2 == 0:
        rank = 7 - rank
    return line + rank


def int2square(s):
    line = s // 8 + 1
    rank = s % 8 + 1
    if line % 2 == 0:
        rank = 9 - rank
    return (line, rank)


def random_different_square(s):
    num = square2int(s)
    other_num = randint(0, 62)

    if other_num >= num:
        other_num += 1

    return int2square(other_num)


def random_different_bishop_square(s):
    num = square2int(s)
    other_num = randint(0, 30)

    if other_num >= num // 2:
        other_num += 1

    return int2square(other_num * 2 + num % 2)


def shift_square(s, shift):
    return (s[0] + shift[0], s[1] + shift[1])


def knight_jumps(s):
    relative_jumps = [
        [-2, -1],
        [-2, 1],
        [-1, -2],
        [-1, 2],
        [1, -2],
        [1, 2],
        [2, -1],
        [2, 1],
    ]
    all_jumps = [shift_square(s, shift) for shift in relative_jumps]

    return filter_illegal_squares(all_jumps)


def is_valid_knight_jump(s0, s1):
    return s1 in knight_jumps(s0)


def mutual_bishop_squares(x, y):
    if is_light_square(x) != is_light_square(y):
        raise ValueError("Two squares for a bishop must be on the same colour")

    # Solution of the equation system
    # x0 + c1 * 1 + c2 * (-1) = y0
    # x1 + c1 * 1 + c2 *   1  = y1
    c1 = (y[0] + y[1] - (x[0] + x[1])) // 2
    c2 = (y[1] - y[0] - (x[1] - x[0])) // 2

    if c1 == 0 or c2 == 0:  # both squares are on the same diagonal
        return []

    return filter_illegal_squares(
        [shift_square(x, [c1, c1]), shift_square(x, [-c2, c2])]
    )


def format_square(s):
    letters = "abcdefgh"
    return letters[s[0] - 1] + str(s[1])


def format_list(square_list):
    return ", ".join([format_square(s) for s in square_list])


def parse_square(s):
    letters = "abcdefgh"
    stripped = s.strip().lower()

    msg = "{} is not a valid square".format(stripped)

    if len(stripped) != 2:
        raise ValueError(msg)

    line = letters.find(stripped[0]) + 1
    if line == 0:
        raise ValueError(msg)
    try:
        rank = int(stripped[1])
    except ValueError:
        raise ValueError(msg)

    if not (1 <= rank <= 8):
        raise ValueError(msg)

    return (line, rank)


def parse_list(square_list):
    result = []
    err_list = []

    if not square_list:
        return result

    str_squares = re.split("[,\\s]", square_list)
    str_squares = [s.strip() for s in str_squares]
    str_squares = [s for s in str_squares if s]
    print(str_squares)

    for s in str_squares:
        try:
            parsed = parse_square(s)
            result.append(parsed)
        except ValueError as err:
            err_list.append(str(err))

    if len(err_list) >= 1:
        raise ValueError(" - " + "\n - ".join(err_list))

    return result


def evaluate_list_answer(answer, solution):
    try:
        as_list = parse_list(answer)
    except ValueError as err:
        if len(answer) != 1 and answer not in "qsh":
            print(str(err))
        return [False, [], [], []]

    correct_squares = []
    wrong_squares = []
    missing_squares = []

    for square in as_list:
        if square in solution:
            correct_squares.append(square)
        else:
            wrong_squares.append(square)

    for square in solution:
        if square not in as_list:
            missing_squares.append(square)

    return [True, correct_squares, wrong_squares, missing_squares]
