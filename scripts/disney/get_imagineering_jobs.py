import re
import os
import requests
import time
import numpy as np
import pandas as pd
from datetime import date

from bs4 import BeautifulSoup


def save(df, cache_path):
    if not os.path.exists(cache_path):
        df.to_csv(cache_path, index=False)
        return df

    df_gospel = pd.read_csv(cache_path)
    df_gospel['cat_id'] = df_gospel['cat_id'].astype(int)
    df_gospel['job_id'] = df_gospel['job_id'].astype(int)
    df_gospel['date'] = pd.to_datetime(df.date)

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

    df_new.to_csv(cache_path, index=False)
    return df_new

def parse(cache_path):
    p = 1
    total = 20

    jobs = []
    while p <= total:
        url = f'https://jobs.disneycareers.com/search-jobs?k=imagineering&p={p}'
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

        p += 1
        time.sleep(5)

    df = pd.DataFrame(jobs)
    df['cat_id'] = df['cat_id'].astype(int)
    df['job_id'] = df['job_id'].astype(int)
    df['date'] = pd.to_datetime(df.date)

    output_df = save(df, cache_path)
    print(f'saved #{len(output_df)} records')


if __name__ == '__main__':
    parse('./data/disney/jobs.csv')
