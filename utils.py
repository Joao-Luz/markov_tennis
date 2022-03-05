import pandas as pd

def matches_won(df : pd.DataFrame):
    a_matches = 0
    b_matches = 0

    for match in df['match'].unique():
        df_match = df[df['match'] == match]

        a_sets, b_sets = sets_won(df_match)

        if a_sets == 2:
            a_matches += 1
        else:
            b_matches += 1
    
    return a_matches, b_matches

def sets_won(df : pd.DataFrame):
    a_sets = 0
    b_sets = 0

    for match in df['match'].unique():
        df_match = df[df['match'] == match]
        for set in df_match['set'].unique():
            df_set = df_match[df_match['set'] == set]
            a_games, b_games = games_won(df_set)

            # 7x5 7x6 6x..
            if a_games == 7 or (a_games == 6 and b_games < 5):
                a_sets += 1
            else:
                b_sets += 1
            
    return a_sets, b_sets

def games_won(df : pd.DataFrame):
    a_games = len(df[df['state'] == 'win_a'])
    b_games = len(df[df['state'] == 'win_b'])
    return a_games, b_games

def points_scored(df : pd.DataFrame):
    a_points = len(df[df['point'] == 'a'])
    b_points = len(df[df['point'] == 'b'])
    return a_points, b_points
