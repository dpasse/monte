import re
import os
import sys
import requests
import time
import numpy as np
import pandas as pd
from datetime import date

from bs4 import BeautifulSoup


search_parameters = {
    'imagineering': 'ascf=[%7B%22key%22:%22custom_fields.IndustryCustomField%22,%22value%22:%22Walt+Disney+Imagineering%22%7D]',
}


def save(df, cache_path):
    if not os.path.exists(cache_path):
        df.sort_values(['date', 'cat_id', 'job_id'], ascending=True).to_csv(cache_path, index=False)
        return df

    df_gospel = pd.read_csv(cache_path)
    df_gospel['cat_id'] = df_gospel['cat_id'].astype(int)
    df_gospel['job_id'] = df_gospel['job_id'].astype(int)
    df_gospel['date'] = pd.to_datetime(df_gospel['date'])

    ## add date, close?
    df_gospel_slim = df_gospel[['cat_id', 'job_id']]
    df_scrapped_new = df \
        .merge(df_gospel_slim, indicator='i', how='outer')

    closed_jobs = df_scrapped_new.query('i == "right_only"')[['cat_id', 'job_id']]
    df_scrapped_new = df_scrapped_new.query('i == "left_only"').drop(['i'], axis=1)

    if not df_scrapped_new.empty:
        df_new = pd.concat([df_gospel, df_scrapped_new], axis=0)
    else:
        df_new = df_gospel.copy()

    for _, row in closed_jobs.iterrows():
        cat_id = row['cat_id']
        job_id = row['job_id']
        q = np.logical_and(df_new['cat_id'] == cat_id, df_new['job_id'] == job_id)
        q = np.logical_and(q, df_new['close'] == '-')
        df_new.loc[q, 'close'] = date.today()

    df_new.sort_values(['date', 'cat_id', 'job_id'], ascending=True).to_csv(cache_path, index=False)
    return df_new

def parse(cache_path, search_type='all'):
    p = 1
    total = 20

    query_parameters = '&'
    if search_type in search_parameters:
        query_parameters += search_parameters[search_type]
    else:
        query_parameters += 'k=imagineering'

    jobs = []
    while p <= total:
        url = f'https://jobs.disneycareers.com/search-jobs?p={p}{query_parameters}'
        response = requests.get(url)

        if response.status_code != 200:
            print(f'** ran into an issue {response.status_code}')
            break

        bs = BeautifulSoup(
            response.content,
            features='html.parser'
        )

        total = int(
            re.sub('of\s+', '', bs.select('.pagination-total-pages')[0].text)
        )

        rows = bs.select('#search-results-list tr')
        if len(rows) == 0:
            print('no rows to parse, stopping')
            break

        for row in bs.select('#search-results-list tr'):
            cols = row.select('td')
            if len(cols) < 3:
                continue

            link = cols[0].select('a')[0].attrs['href']
            cat_id = re.search(r'(?<=\/)(\d+)(?=\/\d+$)', link)
            job_id = re.search(r'(?<=\/)(\d+)$', link)

            jobs.append({
                'cat_id': cat_id.group(0),
                'job_id': job_id.group(0),
                'title': re.sub('\s+', ' ', cols[0].text).strip(),
                'date': re.sub('\s+', ' ', cols[1].text).strip(),
                'brand': re.sub('\s+', ' ', cols[2].text).strip(),
                'location': re.sub('\s+', ' ', cols[3].text).strip(),
                'url': f'https://jobs.disneycareers.com{link}',
                'close': '-'
            })


        print(f'    - completed: {p} / {total}')

        p += 1
        time.sleep(5)

    df = pd.DataFrame(jobs)
    df['cat_id'] = df['cat_id'].astype(int)
    df['job_id'] = df['job_id'].astype(int)
    df['date'] = pd.to_datetime(df.date)

    output_df = save(df, cache_path)
    print(f'saved #{len(output_df)} records')


if __name__ == '__main__':
    search_type = ''
    if len(sys.argv) == 2:
        search_type = sys.argv[1]

    if not os.path.exists('./data'):
        os.mkdir('./data')

    if not os.path.exists('./data/disney'):
        os.mkdir('./data/disney')

    file_name_prefix = '' if search_type == '' else f'{search_type}_'
    parse(f'./data/disney/{file_name_prefix}jobs.csv', search_type)
