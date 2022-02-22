import sys
import requests
import pandas

from bs4 import BeautifulSoup


def main(year):
    data = []
    output_file = f'./data/nfl/pfr-{year}-games.csv'
    url = f'https://www.pro-football-reference.com/years/{year}/games.htm'

    response = requests.get(url)
    assert response.status_code == 200

    bs = BeautifulSoup(response.content, features='html.parser')
    rows = bs.find(id='div_games').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 0:
            continue

        week = row.find_all('th')[0].text

        win_obj = cols[3].find('a')
        if win_obj is None:
            continue

        lose_obj = cols[5].find('a')
        if lose_obj is None:
            continue

        t1_pts = int(cols[7].text)
        t2_pts = int(cols[8].text)

        data.append({
            'week': week,
            'team': win_obj.text,
            'pf': t1_pts,
            'pa': t2_pts,
            'yards': int(cols[9].text),
            'turnovers': int(cols[10].text),
            'played': lose_obj.text,
        })

        data.append({
            'week': week,
            'team': lose_obj.text,
            'pf': t2_pts,
            'pa': t1_pts,
            'yards': int(cols[11].text),
            'turnovers': int(cols[12].text),
            'played': win_obj.text,
        })

    pandas.DataFrame(data).to_csv(output_file)

if __name__ == '__main__':
    year = sys.argv[1]
    main(year)
