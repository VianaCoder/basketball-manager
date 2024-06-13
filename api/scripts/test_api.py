import requests
import uuid

BASE_URL = 'http://localhost:8000'
LOGIN_URL = f'{BASE_URL}/login/'
PLAYERS_URL = f'{BASE_URL}/players/'
REGISTER_URL = f'{BASE_URL}/user/'
TEAMS_URL = f'{BASE_URL}/teams/'

def get_auth_token(username, password):
    response = requests.post(LOGIN_URL, data={'username': username, 'password': password})
    response.raise_for_status()
    return response.json()['token']

def get_high_scorers(token):
    response = requests.get(f'{PLAYERS_URL}high-scorers/', headers={'Authorization': f'Token {token}'})
    if response.status_code != 200:
        print(f'Failed to get high scorers: {response.status_code}')
        print(f'Response: {response.json()}')
    response.raise_for_status()
    return response.json()

def players_from_your_team(token):
    response = requests.get(f'{PLAYERS_URL}', headers={'Authorization': f'Token {token}'})
    if response.status_code != 200:
        print(f'Failed to get players: {response.status_code}')
        print(f'Response: {response.json()}')
    response.raise_for_status()
    return response.json()

def test_authorization_in_teams(token):
    response = requests.get(f'{TEAMS_URL}', headers={'Authorization': f'Token {token}'})
    if response.status_code != 403:
        print(f'Failed in authorization control')
    return ("Sucess to test authorization")

def main():
    
    existing_coach_username = 'coach1'  
    coach_password = 'password123'  

    token = get_auth_token(existing_coach_username, coach_password)
    print(f'Coach token: {token}')

    high_scorers = get_high_scorers(token)
    print(f'High scorers: {high_scorers}')

    coached_team_players = players_from_your_team(token)
    print(f'Players: {coached_team_players}')

    all_teams = test_authorization_in_teams(token)
    print(f'Players: {all_teams}')

if __name__ == '__main__':
    main()
