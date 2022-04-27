import sys
import requests
import pandas

from bs4 import BeautifulSoup


def main(year):
    data = []
    combo = []
    output_file = f'./data/nfl/pfr-{year}-games.csv'
    combo_output_file = f'./data/nfl/pfr-{year}-games-combo.csv'
    url = f'https://www.pro-football-reference.com/years/{year}/games.htm'

    response = requests.get(url)
    assert response.status_code == 200

    bs = BeautifulSoup(response.content, features='html.parser')
    rows = bs.find(id='games').find('tbody').find_all('tr')
    for row in rows:
        cls = row.get('class')
        if cls is not None:
            continue

        cols = row.find_all('td')
        if len(cols) == 0:
            continue

        week = row.find_all('th')[0].text

        win_obj = cols[3].find('a')
        if win_obj is None:
            continue

        at = cols[4].text.strip()

        lose_obj = cols[5].find('a')
        if lose_obj is None:
            continue

        t1_pts = int(cols[7].text)
        t2_pts = int(cols[8].text)

        winner = {
            'week': week,
            'team': win_obj.text,
            'is_home_team': at == '',
            'pf': t1_pts,
            'pa': t2_pts,
            'yards': int(cols[9].text),
            'turnovers': int(cols[10].text),
            'played': lose_obj.text,
        }

        data.append(winner)

        loser = {
            'week': week,
            'team': lose_obj.text,
            'is_home_team': at == '@',
            'pf': t2_pts,
            'pa': t1_pts,
            'yards': int(cols[11].text),
            'turnovers': int(cols[12].text),
            'played': win_obj.text,
        }

        data.append(loser)

        if winner['is_home_team']:
            combo.append({
                'week': week,
                'home': winner['team'],
                'home_pts': winner['pf'],
                'away': loser['team'],
                'away_pts': loser['pf']
            })
        elif loser['is_home_team']:
            combo.append({
                'week': week,
                'home': loser['team'],
                'home_pts': loser['pf'],
                'away': winner['team'],
                'away_pts': winner['pf'],
            })

    pandas.DataFrame(data).to_csv(output_file)
    pandas.DataFrame(combo).to_csv(combo_output_file)


if __name__ == '__main__':
    year = sys.argv[1]
    main(year)
