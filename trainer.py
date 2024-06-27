#!/usr/bin/env python3

# A simple chess visualization trainer
#
# Copyright 2024, cretaceum, MIT license


from random import randint, seed


def filter_illegal_squares(squares):
    filtered = []
    for s in squares:
        if 1 <= s[0] <= 8 and 1 <= s[1] <= 8:
            filtered.append(s)
    return filtered


def is_light_square(s):
    return (s[0] + s[1]) % 2 == 1


def random_square():
    return [randint(1, 8), randint(1, 8)]


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
    return [line, rank]


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
    return [s[0] + shift[0], s[1] + shift[1]]


def knight_jumps(s):
    relative_jumps = [[-2, -1], [-2, 1], [-1, -2], [-1, 2],
                      [1, -2], [1, 2], [2, -1], [2, 1]]
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

    return filter_illegal_squares([shift_square(x, [c1, c1]), shift_square(x, [-c2, c2])])


def write_square(s):
    letters = "abcdefgh"
    return letters[s[0] - 1] + str(s[1])


def read_square(s):
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

    return [line, rank]


def print_help():
    msg = """You can type the following letters at any time:

 - q to exit,
 - s to skip an answer,
 - or h to see this message.\n"""
    print(msg)


class GameEndException(Exception):
    pass


def check_yn_answer(query, yes_is_correct):
    answer = input(query).lower().strip()
    while len(answer) != 1 or "ynqs".find(answer) == -1:
        if answer == "h":
            print_help()
        else:
            print("Try again! Answer with y or n, s to skip, or h for help.")
        answer = input(query).lower().strip()

    if answer == "q":
        raise GameEndException

    if answer == "s":
        if yes_is_correct:
            print("It is a light square.")
        else:
            print("It is a dark square.")
        return

    if (answer == "y") == yes_is_correct:
        print("Correct!")
    else:
        print("Wrong.")


def read_list(square_list):
    result = []
    err_list = []

    if len(square_list) == 0:
        return result

    if square_list.find(",") != -1:
        str_squares = square_list.split(", ")
    else:
        str_squares = square_list.split(" ")

    for s in str_squares:
        if len(s.strip()) == 0:
            continue
        try:
            parsed = read_square(s)
            result.append(parsed)
        except ValueError as err:
            err_list.append(str(err))

    if len(err_list) >= 1:
        raise ValueError(" - " + "\n - ".join(err_list))

    return result


def write_list(square_list):
    return ", ".join([write_square(s) for s in square_list])


def evaluate_list_answer(answer, solution):
    try:
        as_list = read_list(answer)
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


def check_list_answer(query, solution):
    response = input(query).lower().strip()
    syntax, correct, wrong, missing = evaluate_list_answer(response, solution)

    while True:
        if syntax:
            if len(wrong) != 0:
                print(" - incorrect: " + write_list(wrong))
            if len(missing) != 0:
                print(" - missing: " + write_list(missing))
            if len(wrong) == 0 and len(missing) == 0:
                print("Correct!")
            return

        if response == "q":
            raise GameEndException
        if response == "s":
            print("The answer is:  {}".format(write_list(solution)))
            return
        if response == "h":
            print_help()

        response = input(query).lower().strip()
        syntax, correct, wrong, missing = evaluate_list_answer(response, solution)


def check_knight_tour(query, s, u):
    response = input(query).lower().strip()
    while True:
        try:
            tour = read_list(response)
            break
        except ValueError as err:
            if len(response) != 1 and response not in "qsh":
                print(str(err))
            else:
                if response == "q":
                    raise GameEndException
                if response == "s":
                    return
                if response == "h":
                    print_help()
        response = input(query).lower().strip()

    failed = False
    prev = s
    if len(tour) == 0 or tour[-1] != u:
        tour.append(u)
    for j in tour:
        if not is_valid_knight_jump(prev, j):
            print(" - illegal move from {} to {}".format(write_square(prev), write_square(j)))
            failed = True
        prev = j
    if not failed:
        print("Correct!")


def main():
    seed()
    print("Visualization trainer.\n")
    print_help()
    try:
        while True:
            s = random_square()
            check_yn_answer("Is {} a light square? [y/n]\n".format(write_square(s)), is_light_square(s))
            check_list_answer("List all knight jumps from {} (e.g. c2, b3).\n".format(write_square(s)), knight_jumps(s))

            t = random_different_square(s)
            check_knight_tour("Give a knight tour from {} to {}.\n".format(write_square(s), write_square(t)), s, t)

            u = random_different_bishop_square(s)
            q = "List all transfer squares for a bishop from {} to {} (leave empty if on same diagonal).\n"
            check_list_answer(q.format(write_square(s), write_square(u)), mutual_bishop_squares(s, u))

    except GameEndException:
        print("Good bye.")


if __name__ == '__main__':
    main()
