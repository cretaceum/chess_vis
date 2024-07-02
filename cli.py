#!/usr/bin/env python3

# A simple chess visualization trainer
#
# Copyright 2024, cretaceum, MIT license

from random import seed

from chess_vis.shared import (
    random_square,
    format_square,
    format_list,
    parse_list,
    evaluate_list_answer,
    is_valid_knight_jump,
    is_light_square,
    knight_jumps,
    mutual_bishop_squares,
    random_different_square,
    random_different_bishop_square,
    GameEndException,
)


def print_help():
    msg = """You can type the following letters at any time:

 - q to exit,
 - s to skip an answer,
 - or h to see this message.\n"""
    print(msg)


def check_knight_tour(query, s, u):
    response = input(query).lower().strip()
    while True:
        try:
            tour = parse_list(response)
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
    if len(tour) == 0 or tour[-1] != u:
        tour.append(u)
    if tour[0] == s:
        prev = None
    else:
        prev = s
    for j in tour:
        if prev is None:
            continue
        if not is_valid_knight_jump(prev, j):
            print(
                " - illegal move from {} to {}".format(
                    format_square(prev), format_square(j)
                )
            )
            failed = True
        prev = j
    if not failed:
        print("Correct!")


def check_list_answer(query, solution):
    response = input(query).lower().strip()
    syntax, correct, wrong, missing = evaluate_list_answer(response, solution)

    while True:
        if syntax:
            if len(wrong) != 0:
                print(" - incorrect: " + format_list(wrong))
            if len(missing) != 0:
                print(" - missing: " + format_list(missing))
            if len(wrong) == 0 and len(missing) == 0:
                print("Correct!")
            return

        if response == "q":
            raise GameEndException
        if response == "s":
            print("The answer is:  {}".format(format_list(solution)))
            return
        if response == "h":
            print_help()

        response = input(query).lower().strip()
        syntax, correct, wrong, missing = evaluate_list_answer(response, solution)


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


def main():
    seed()
    print("Visualization trainer.\n")
    print_help()
    try:
        while True:
            s = random_square()
            check_yn_answer(
                "Is {} a light square? [y/n]\n".format(format_square(s)),
                is_light_square(s),
            )
            check_list_answer(
                "List all knight jumps from {} (e.g. c2, b3).\n".format(
                    format_square(s)
                ),
                knight_jumps(s),
            )

            t = random_different_square(s)
            check_knight_tour(
                "Give a knight tour from {} to {}.\n".format(
                    format_square(s), format_square(t)
                ),
                s,
                t,
            )

            u = random_different_bishop_square(s)
            q = "List all transfer squares for a bishop from {} to {} (leave empty if on same diagonal).\n"
            check_list_answer(
                q.format(format_square(s), format_square(u)),
                mutual_bishop_squares(s, u),
            )

    except GameEndException:
        print("Good bye.")


if __name__ == "__main__":
    main()
