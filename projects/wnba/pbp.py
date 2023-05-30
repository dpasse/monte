import json
import time
import requests

from bs4 import BeautifulSoup

from bb.filesystem import load_data, save_data

TIMEOUT_IN_SECONDS = 4
JSON_TAG = "window['__espnfitt__']="


def get_pbp(game_id: str):
    response = requests.get(
        f'https://www.espn.com/wnba/game/_/gameId/{game_id}'
    )

    scripts = BeautifulSoup(response.text, features='html.parser') \
        .select('script')

    js = [
        script
        for script in scripts
        if script.text.startswith(JSON_TAG)
    ][0].text.replace(JSON_TAG, '')[:-1]

    order = 1
    obj = json.loads(js)
    pbp = obj['page']['content']['gamepackage']['shtChrt']

    home_id = pbp['tms']['home']['id']
    away_id = pbp['tms']['away']['id']
    is_neutral_site = pbp['ntrlSte']

    order = 0
    shot_chart = []
    for event in pbp['plays']:
        athlete = event['athlete']
        shot_chart.append({
            'game_id': game_id,
            'team_id': away_id if 'away' == event['homeAway'] else home_id,
            'player': {
                'id': athlete['id'],
                'name': athlete['name'] if 'name' in athlete else '',
            },
            'homeAway': event['homeAway'],
            'is_neutral_site': is_neutral_site,
            'quarter': event['period']['number'],
            'location': {
                'x': event['coordinate']['x'],
                'y': event['coordinate']['y'],
            },
            'text': event['text'],
            'made': event['scoringPlay'] if 'scoringPlay' in event else False,
            'order': order,
        })

    return shot_chart

def run(games):
    for game in games:
        game_id = game['game_id']

        game['pbp'] = get_pbp(game_id)

        save_data(
            f'./data/pbps/{game_id}.json',
            game
        )

        time.sleep(TIMEOUT_IN_SECONDS)

if __name__ == '__main__':
    run(
        load_data('./data/games.json')
    )
