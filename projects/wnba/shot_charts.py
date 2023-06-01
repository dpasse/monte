import json
import time
import requests

from bs4 import BeautifulSoup

from bb.utils.filesystem import load_data, save_data

TIMEOUT_IN_SECONDS = 10
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

    home = {
        'id': pbp['tms']['home']['id'],
        'abbr': pbp['tms']['home']['abbrev']
    }

    away = {
        'id': pbp['tms']['away']['id'],
        'abbr': pbp['tms']['away']['abbrev']
    }

    is_neutral_site = pbp['ntrlSte']

    order = 0
    shot_chart = []
    for event in pbp['plays']:
        athlete = event['athlete']
        shot_type = event['type']
        shot_chart.append({
            'team': away if 'away' == event['homeAway'] else home,
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
            'type': {
                'id': shot_type['id'],
                'text': shot_type['txt'],
            }
        })

    return shot_chart

def run(games):
    for game in games:
        game_id = game['game_id']

        print(game_id)

        game['shots'] = get_pbp(game_id)

        save_data(
            f'./data/pbps/{game_id}.json',
            game
        )

        time.sleep(TIMEOUT_IN_SECONDS)


if __name__ == '__main__':
    run(
        load_data('./data/games.json')
    )
