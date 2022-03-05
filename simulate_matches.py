import random

def choice(p : float, choice_a : str, choice_b : str) -> str:
    if random.random() <= p:
        return choice_a, 'a'
    else:
        return choice_b, 'b'

def simulate_game(p : float):
    states = []
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
        
        states.append(current_state)
        points.append(point)
        current_state = next_state

    states.append(current_state)
    return (current_state[-1], states, points)

def simulate_tie_break(p : float):
    pa = pb = 0
    points = []
    states = []
    while True:
        if random.random() < p:
            pa += 1
            points.append('a')
        else:
            pb += 1
            points.append('b')

        if pa >= 7 and pb <= pa-2:
            states.append('win_a')
            return (states, points)
        elif pb >= 7 and pa <= pb-2:
            states.append('win_b')
            return (states, points)

        states.append('tie-break')


def simulate_set(p : float):

    a_games = b_games = 0
    games = []
    set_winner = None

    while True:
        winner, states, points = simulate_game(p)

        if winner == 'a':
            a_games += 1
        else:
            b_games += 1
        
        games.append([states, points])
        if a_games >= 6 and b_games <= a_games-2:
            # a wins
            set_winner = 'a'
            break
        elif b_games >= 6 and a_games <= b_games-2:
            # b wins
            set_winner = 'b'
            break
        elif a_games == b_games == 6:
            states, points = simulate_tie_break(p)
            games.append([states, points])
            break
    
    return set_winner, games
        
    

def simulate_match(p : float, n : int = 1):
    assert type(p) is float and (p >= 0 and p <= 1), "Parameter p must be a real number between 0 and 1"
    matches = []
    win_a = win_b = 0
    for _ in range(n):
        a_wins = 0
        b_wins = 0
        game = 0
        sets = []
        while (a_wins != 2 and b_wins != 2):
            (winner, games) = simulate_set(p)
            if winner == 'a': a_wins += 1
            else: b_wins += 1

            sets.append(games)

            game += 1
        winner = 'a' if a_wins == 2 else 'b'
        if winner == 'a': win_a += 1
        if winner == 'b': win_b += 1
        matches.append(sets)
    
    print(win_a, win_b)
    return matches

def simulate_matches(output_dir, p, n):
    matches = simulate_match(p, n=n)
    with open(output_dir, 'w') as output:
        output.write('match,set,game,play,state,point\n')
        for i,match in enumerate(matches):
            for j,set in enumerate(match):
                for k,game in enumerate(set):
                    for l,(play,point) in enumerate(zip(game[0], game[1])):
                        output.write(f'{i},{j},{k},{l},{play},{point}\n')

import sys
if __name__ == '__main__':
    output_dir = sys.argv[1]
    p = float(sys.argv[2])
    n = int(sys.argv[3])
    simulate_matches(output_dir, p, n)
