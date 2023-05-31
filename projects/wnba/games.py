import re
import time
import requests

from typing import List
from bs4 import BeautifulSoup
from bb.utils.filesystem import load_data, save_data


TIMEOUT_IN_SECONDS = 4

def parse(html):
    games = []

    rows = BeautifulSoup(html, features='html.parser').select('.Table__TR')
    for tr in rows:
        cols = [
            col
            for col in tr.select('td:not(.ttu)')
        ]

        if len(cols) != 7:
            continue

        game_id = ''
        links = cols[2].select('.AnchorLink')
        if len(links) != 0:
            game_id = re.search(r'\/gameId\/(\w+)$', links[0].get('href')).group(1)

        games.append({
            'date': re.sub(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), ', '', cols[0].text),
            'game_id': game_id,
        })

    return games

def get_games_by_team(team_id: str, years: List[str]):
    games = []
    for year in years:
        response = requests.get(
            f'https://www.espn.com/wnba/team/schedule/_/name/{team_id}/season/{year}'
        )

        team_games = parse(response.text)
        for game in team_games:
            game.update({ 'year': year, 'team_id': team_id })

        games.extend(team_games)

        time.sleep(TIMEOUT_IN_SECONDS)

    return games

if __name__ == '__main__':
    years = [
        2022
    ]

    games = {}
    for team in load_data('./data/teams.json'):
        team_id = team['id']
        abbr = team['abbr']

        for game in get_games_by_team(abbr, years):
            date = game['date']
            game_id = game['game_id']
            year = game['year']

            if not game_id in games:
                games[game_id] = {
                    'date': date,
                    'game_id': game_id,
                    'year': year,
                    'teams': [team_id]
                }
            else:
                games[game_id]['teams'].append(team_id)

    save_data(
        './data/games.json',
        list(games.values())
    )
