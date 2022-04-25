import sys
import json
import requests
import itertools


def get_league_rosters(season, league_id):
    def get_rosters(season, league_id):
        url = f'https://fantasy.espn.com/apis/v3/games/flb/seasons/{season}/segments/0/leagues/{league_id}?view=mRoster&view=mTeam'
        return requests.get(url).json()['teams']

    def get_player(entry, fullname):
        player = entry['playerPoolEntry']['player']
        response = {
            'id': player['id'],
            'name': player['fullName'],
            'is_a': [],
            'is_on': fullname,
        }

        slots = player['eligibleSlots']
        if any(filter(lambda x: x >= 13 and x <= 15, slots)):
            response['is_a'].append('PITCHER')

        if any(filter(lambda x: x < 13, slots)):
            response['is_a'].append('BATTER')

        return response

    teams = []
    for roster in get_rosters(season, league_id):
        location = roster['location']
        nickname = roster['nickname']
        fullname = f'{location} {nickname}'
        teams.append({
            'name': fullname,
            'roster': [
                get_player(entry, fullname)
                for entry
                in roster['roster']['entries']
            ],
        })

    return teams

def main(season, league_id):
    teams = get_league_rosters(season, league_id)

    output_file = f'./data/mlb/roster-{league_id}.json'
    with open(output_file, 'w') as output:
        output.write(
            json.dumps(teams, indent=3)
        )

    output_file = f'./data/mlb/roster-{league_id}-as-graph.json'
    with open(output_file, 'w') as output:
        players = list(
            itertools.chain.from_iterable(
                map(lambda team: team['roster'], teams)
            )
        )
        output.write(
            json.dumps(players, indent=3)
        )


if __name__ == '__main__':
    year = sys.argv[1] ## '2022'
    league_id = sys.argv[2] ## '853208662'

    main(year, league_id)
