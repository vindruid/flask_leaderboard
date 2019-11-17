import pandas as pd

leaderboard = pd.read_csv('dummy_tables.csv')

for ix, (_, row) in enumerate(leaderboard.iterrows()):
    print(row.team_name)
    print(ix)