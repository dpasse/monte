import re
import json
import requests

from bs4 import BeautifulSoup

from bb.filesystem import save_data


def parse(html):
    rows = BeautifulSoup(html, features='html.parser') \
        .select('.standings__table div.team-link .dn')
    
    teams = []
    for row in rows:
        abbr = row.select('abbr')[0]
        link = row.select('a.AnchorLink')[0].get('href')
        team_id = re.search(
            r'\/(?:name)\/(.+)',
            link
        ).group(1)

        teams.append({
            'id': team_id,
            'abbr': abbr.text,
            'title': abbr.get('title')
        })

    return teams

def get_teams():
    response = requests.get('https://www.espn.com/wnba/standings')
    assert response.status_code == 200

    save_data('./data/teams.json', parse(response.text))

if __name__ == '__main__':
    get_teams()
