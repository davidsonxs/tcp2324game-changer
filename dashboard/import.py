import csv
from dashboard.models import Game
from dashboard.utils import read_csv_file

file_path = 'nhl_pbp_20202021.csv'
games_data = read_csv_file(file_path)

for game_data in games_data:
    Game.objects.create(
        Away_Score=game_data['Away_Score'],
        Home_Score=game_data['Home_Score'],
        Away_Goalie=game_data['Away_Goalie'],
        Home_Goalie=game_data['Home_Goalie'],
        Event=game_data['Event'],
        Period=int(game_data['Period']),
        Ev_Zone=game_data['Ev_Zone'],
        Strength=game_data['Strength'],
        Type=game_data['Type'],
        Date=game_data['Date'],
        Ev_Team=game_data['Ev_Team'],
        Away_Team=game_data['Away_Team'],
        Home_Team=game_data['Home_Team']
    )