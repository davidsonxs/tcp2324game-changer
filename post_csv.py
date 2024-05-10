import csv
import requests


def import_games(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                out = requests.post("http://localhost:8000/create/", timeout=0.01, data={
                    'Away_Score': row['Away_Score'],
                    'Home_Score': row['Home_Score'],
                    'Away_Goalie': row['Away_Goalie'],
                    'Home_Goalie': row['Home_Goalie'],
                    'Event': row['Event'],
                    'Period': row['Period'],
                    'Ev_Zone': row['Ev_Zone'],
                    'Strength': row['Strength'],
                    'Type': row['Type'],
                    'Date': row['Date'],
                    'Ev_Team': row['Ev_Team'],
                    'Away_Team': row['Away_Team'],
                    'Home_Team': row['Home_Team']})
                print(out.text)
            except Exception as e:
                pass


if __name__ == '__main__':
    csv_file_path = 'dashboard/nhl_pbp_20202021.csv'
    import_games(csv_file_path)
