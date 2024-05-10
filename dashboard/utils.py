import csv
from .models import Game


def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extracting values for each column
            away_score = row.get('Away_Score')
            home_score = row.get('Home_Score')
            away_goalie = row.get('Away_Goalie')
            home_goalie = row.get('Home_Goalie')
            event = row.get('Event')
            period = row.get('Period')
            ev_zone = row.get('Ev_Zone')
            strength = row.get('Strength')
            game_type = row.get('Type')  # Changed variable name to game_type
            date = row.get('Date')
            ev_team = row.get('Ev_Team')
            away_team = row.get('Away_Team')
            home_team = row.get('Home_Team')

            # Constructing a dictionary for each row and appending it to the data list
            data.append({
                'Away_Score': away_score,
                'Home_Score': home_score,
                'Away_Goalie': away_goalie,
                'Home_Goalie': home_goalie,
                'Event': event,
                'Period': period,
                'Ev_Zone': ev_zone,
                'Strength': strength,
                'Type': game_type,
                'Date': date,
                'Ev_Team': ev_team,
                'Away_Team': away_team,
                'Home_Team': home_team
            })
    return data
