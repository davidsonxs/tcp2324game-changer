from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Game
import datetime


# Create your views here.
def index(request):
    return HttpResponse("<div><h1><3></h1></div>")


def game_list(request):
    games = Game.objects.all()
    serialized_games = []
    for game in games:
        serialized_games.append({
            'Away_Score': game.Away_Score,
            'Home_Score': game.Home_Score,
            'Away_Goalie': game.Away_Goalie,
            'Home_Goalie': game.Home_Goalie,
            'Event': game.Event,
            'Period': game.Period,
            'Ev_Zone': game.Ev_Zone,
            'Strength': game.Strength,
            'Type': game.Type,
            'Date': game.Date.strftime('%Y-%m-%d'),  # Format date as string
            'Ev_Team': game.Ev_Team,
            'Away_Team': game.Away_Team,
            'Home_Team': game.Home_Team
        })
    return JsonResponse({'games': serialized_games})


@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        try:
            data = request.POST
            print(data)
            # Creating a new game entry
            Game.objects.create(
                Away_Score=int(data.get('Away_Score')),
                Home_Score=int(data.get('Home_Score')),
                Away_Goalie=data.get('Away_Goalie'),
                Home_Goalie=data.get('Home_Goalie'),
                Event=data.get('Event'),
                Period=int(data.get('Period')),
                Ev_Zone=data.get('Ev_Zone'),
                Strength=data.get('Strength'),
                Type=data.get('Type'),
                Date=datetime.datetime(int(data.get('Date').split('-')[0]), int(data.get('Date').split('-')[1]),
                                       int(data.get('Date').split('-')[2])),
                Ev_Team=data.get('Ev_Team'),
                Away_Team=data.get('Away_Team'),
                Home_Team=data.get('Home_Team'),
            )
            return JsonResponse({'message': 'Games created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def home_away_goals(request):
    if request.method == 'GET':
        team = dict(request.GET)['team'][0]
        data_home = Game.objects.filter(Event='GEND', Home_Team=team)
        data_away = Game.objects.filter(Event='GEND', Away_Team=team)
        ret_dict = {'home': 0, 'away': 0, 'team': team}
        for game in data_home:
            ret_dict['home'] += game.Home_Score
        for game in data_away:
            ret_dict['away'] += game.Away_Score
        return JsonResponse(ret_dict)


def faceoff_wins_per_team_per_period(request):
    if request.method == 'GET':
        team = dict(request.GET)['team'][0]
        period_data = {}
        for period in range(1, 4):  # There are 3 periods in a game
            faceoff_wins = Game.objects.filter(Event='FAC', Ev_Team=team, Period=period).count()
            period_data[period] = {
                'faceoff_wins': faceoff_wins
            }
        return JsonResponse(period_data)


def team_period_performance(request):
    if request.method == 'GET':
        team = request.GET.get('team', None)

        if team:
            data_home = Game.objects.filter(Event='GOAL', Home_Team=team, Period__isnull=False)
            data_away = Game.objects.filter(Event='GOAL', Away_Team=team, Period__isnull=False)

            period_performance = {1: 0, 2: 0, 3: 0, 4: 0, 'team': team}

            for game in data_home:
                period_key = game.Period
                period_performance.setdefault(period_key, 0)
                period_performance[period_key] += 1

            for game in data_away:
                period_key = game.Period
                period_performance.setdefault(period_key, 0)
                period_performance[period_key] += 1

            best_period = max(period_performance, key=lambda k: period_performance[k] if isinstance(k, int) else 0)
            period_performance['best_period'] = best_period

            return JsonResponse(period_performance)
        else:
            return JsonResponse({'error': 'Team not provided'})
    else:
        return JsonResponse({'error': 'Method not allowed'})


def team_performance_by_event(request):
    if 'team' in request.GET:
        team = request.GET['team']
        # Define the list of event types to track
        event_types = ['GOAL', 'BLOCK', 'HIT', 'SHOT', 'PENL', 'GIVE', 'STOP', 'TAKE']
        event_data = {event_type: {'home': 0, 'away': 0} for event_type in event_types}

        # Get all games where the team played as the home or away team
        home_games = Game.objects.filter(Home_Team=team)
        away_games = Game.objects.filter(Away_Team=team)

        # Count occurrences of each event type for home games
        for game in home_games:
            if game.Event in event_data:
                event_data[game.Event]['home'] += 1

        # Count occurrences of each event type for away games
        for game in away_games:
            if game.Event in event_data:
                event_data[game.Event]['away'] += 1

        # Assemble response data
        response_data = {
            'team': team,
            'events': event_data
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No team specified'}, status=400)


def goals_scored_per_team(request):
    if request.method == 'GET':
        all_teams = set(Game.objects.values_list('Away_Team', flat=True)) | set(
            Game.objects.values_list('Home_Team', flat=True))
        goals_data = {team: 0 for team in all_teams}

        for game in Game.objects.all():
            goals_data[game.Away_Team] += game.Away_Score
            goals_data[game.Home_Team] += game.Home_Score

        # Prepare data for the bar chart
        labels = list(goals_data.keys())
        data = list(goals_data.values())

        return JsonResponse({'labels': labels, 'data': data})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def compare_penalties(request):
    teams = set(Game.objects.values_list('Home_Team', flat=True)) | set(Game.objects.values_list('Away_Team', flat=True))
    penalty_data = {team: 0 for team in teams}

    for game in Game.objects.all():
        if game.Event == 'PENL':
            penalty_data[game.Away_Team] += 1
            penalty_data[game.Home_Team] += 1

    return JsonResponse({'penalties': penalty_data})