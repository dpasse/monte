import re
import os
import sys
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


def load_rosters(league_id):
    rosters = {}
    path = f'./data/mlb/roster-{league_id}.json'
    with open(path, 'r') as roster_json:
        for team_roster in json.loads(roster_json.read()):
            roster = { 'batters': [], 'pitchers': [] }
            for player in team_roster['roster']:
                id = player['id']
                name = player['name']

                if 'PITCHER' in player['is_a']:
                    roster['pitchers'].append((id, name))

                if 'BATTER' in player['is_a']:
                    roster['batters'].append((id, name))

            name = team_roster['name']
            rosters[name] = roster

    return rosters

class ScrapPlayers():
    def get_url(self, player_id, category_type):
        category = 'batting' if category_type == 'BATTER' else 'pitching'
        return f'https://www.espn.com/mlb/player/gamelog/_/id/{player_id}/year/2022/category/{category}'

    def transform(self, player, cols, category_type):
        response = {
            'ID': player['id'],
            'NAME': player['name'],
            'DATE': re.sub(r'.+?([\d/]+)', '\g<1>', cols[0].text),
            'OPP': re.sub(r'(@|vs)(.+)', '\g<1> \g<2>', cols[1].text),
            'RESULT': re.sub(r'(W|L)(.+)', '\g<1> \g<2>', cols[2].text),
        }

        if category_type == 'BATTER':
            keys = ['AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'HBP', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS']
        else:
            keys = ['IP', 'H', 'R', 'ER', 'HR', 'BB', 'K', 'GB', 'FB', 'P', 'TBF', 'GSC', 'DEC', 'REL', 'ERA']

        category_stats = { cn: cols[i + 3].text for i, cn in enumerate(keys) }
        return {**response, **category_stats}

    def run(self, players, sleep_time_in_seconds = 5):
        pitchers, batters = [], []
        for player in players:
            id = player['id']
            for is_a in player['is_a']:
                url = self.get_url(id, is_a)
                content = requests.get(url).content
                bs = BeautifulSoup(content, features='html.parser')

                try:
                    rows = bs.select('.mb4 .Table__TBODY tr')
                    stats = [
                        self.transform(player, row.find_all('td'), is_a)
                        for row
                        in rows
                        if not 'totals_row' in row.get('class')
                    ]

                    (batters if is_a == 'BATTER' else pitchers).extend(stats)
                except:
                    print(f'error: {url}')

                time.sleep(sleep_time_in_seconds)

        return pitchers, batters

def save(df, cache_file_path):
    if df.empty:
        return

    def merge(df_gospel, df_scrapped):
        df_gospel_slim = df_gospel[['ID', 'DATE']]
        df_scrapped_new = df_scrapped \
            .merge(df_gospel_slim, indicator='i', how='outer') \
            .query('i == "left_only"') \
            .drop(['i'], axis=1)

        if df_scrapped_new.empty:
            return df_gospel

        return pd.concat([df_gospel, df_scrapped_new], axis=0)

    if not os.path.exists(cache_file_path):
        df.to_csv(cache_file_path, index=False)
        return

    df_gosbel = pd.read_csv(cache_file_path)
    for column in df_gosbel.columns:
        df_gosbel[column] = df_gosbel[column].astype(object)

    for column in df.columns:
        df[column] = df[column].astype(object)

    df_gosbel['ID'] = df_gosbel['ID'].astype(int)
    df['ID'] = df['ID'].astype(int)

    merge(df_gosbel, df).to_csv(cache_file_path, index=False)

def main(players, output_file_name):
    pitchers, batters = ScrapPlayers().run(players)

    batters_file_path = f'./data/mlb/{output_file_name}-batters.csv'
    save(pd.DataFrame(batters), batters_file_path)

    pitchers_file_path = f'./data/mlb/{output_file_name}-pitchers.csv'
    save(pd.DataFrame(pitchers), pitchers_file_path)


if __name__ == '__main__':
    rosters = {}
    league_id = sys.argv[1]
    path = f'./data/mlb/roster-{league_id}.json'
    with open(path, 'r') as roster_json:
        for team_roster in json.loads(roster_json.read()):
            name = team_roster['name']
            rosters[name] = team_roster['roster']

    main(rosters[sys.argv[2]], sys.argv[3]) ## 'Snoring Eeyores'
