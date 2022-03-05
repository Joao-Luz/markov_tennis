import random
from typing import Union
from io import TextIOWrapper

from black import out

def choice(p : float, choice_a : str, choice_b : str) -> str:
    if random.random() < p:
        return choice_a, 'a'
    else:
        return choice_b, 'b'

def simulate_game(p : float, return_plays : bool = False) -> Union[str, tuple]:
    plays = []
    points = ['n']
    current_state = '0-0'
    next_state = None
    while (current_state != 'win_a' and current_state != 'win_b'):
        # next state logic
        if   current_state == '0-0':
            next_state, point = choice(p, '15-love', 'love-15')

        elif current_state == '15-love':
            next_state, point = choice(p, '30-love', '15-15')

        elif current_state == 'love-15':
            next_state, point = choice(p, '15-15', 'love-30')

        elif current_state == '30-love':
            next_state, point = choice(p, '40-love', '30-15')

        elif current_state == '15-15':
            next_state, point = choice(p, '30-15', '15-30')

        elif current_state == 'love-30':
            next_state, point = choice(p, '15-30', 'love-40')

        elif current_state == '40-love':
            next_state, point = choice(p, 'win_a', '40-15')

        elif current_state == '30-15':
            next_state, point = choice(p, '40-15', 'deuce')

        elif current_state == '15-30':
            next_state, point = choice(p, 'deuce', '15-40')

        elif current_state == 'love-40':
            next_state, point = choice(p, '15-40', 'win_b')

        elif current_state == '40-15':
            next_state, point = choice(p, 'win_a', 'adv_a')

        elif current_state == 'deuce':
            next_state, point = choice(p, 'adv_a', 'adv_b')

        elif current_state == '15-40':
            next_state, point = choice(p, 'adv_b', 'win_b')

        elif current_state == 'adv_a':
            next_state, point = choice(p, 'win_a', 'deuce')

        elif current_state == 'adv_b':
            next_state, point = choice(p, 'deuce', 'win_b')
        
        plays.append(current_state)
        points.append(point)
        current_state = next_state

    plays.append(current_state)
    if return_plays:
        return (current_state[-1], plays, points)
    else:
        return current_state[-1]

def simulate_match(p : float, n : int = 1):
    assert type(p) is float and (p >= 0 and p <= 1), "Parameter p must be a real number between 0 and 1"
    matches = []
    for _ in range(n):
        a_wins = 0
        b_wins = 0
        game = 0
        games = []
        while (a_wins != 2 and b_wins != 2):
            (winner, plays, points) = simulate_game(p, return_plays=True)
            if winner == 'a': a_wins += 1
            else: b_wins += 1

            games.append([plays, points])

            game += 1
        winner = 'a' if a_wins == 2 else 'b'
        matches.append(games)
    return matches

def simulate_matches(output_dir, p, n):
    matches = simulate_match(p, n=n)
    with open(output_dir, 'w') as output:
        output.write('match,game,move,play,point\n')
        for i,match in enumerate(matches):
            for j,game in enumerate(match):
                for k,(play,point) in enumerate(zip(game[0], game[1])):
                    output.write(f'{i},{j},{k},{play},{point}\n')

import sys
if __name__ == '__main__':
    output_dir = sys.argv[1]
    p = float(sys.argv[2])
    n = int(sys.argv[3])
    simulate_matches(output_dir, p, n)
