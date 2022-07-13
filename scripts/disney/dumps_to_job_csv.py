import os
import sys
import json
import numpy as np
import pandas as pd

from datetime import date


def merge(df, cache_path):
    df_gospel = pd.read_csv(cache_path)
    df_gospel['cat_id'] = df_gospel['cat_id'].astype(int)
    df_gospel['job_id'] = df_gospel['job_id'].astype(int)
    df_gospel['date'] = pd.to_datetime(df_gospel['date'])

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
        q = np.logical_and(
            np.logical_and(
                df_new['cat_id'] == row['cat_id'],
                df_new['job_id'] == row['job_id']
            ),
            df_new['close'] == '-'
        )

        df_new.loc[q, 'close'] = date.today()

    return df_new

def save(df, cache_path):
    df_new = merge(df, cache_path) if os.path.exists(cache_path) else df
    df_new = df_new.sort_values(['date', 'title', 'cat_id', 'job_id'], ascending=True)
    df_new.to_csv(cache_path, index=False)

    return df_new

def parse(files, cache_path):
    for file in files:
        try:
            with open(file, 'r') as input_file:
                jobs = json.loads(input_file.read())

            df = pd.DataFrame(jobs)

            df['cat_id'] = df['cat_id'].astype(int)
            df['job_id'] = df['job_id'].astype(int)
            df['date'] = pd.to_datetime(df.date)

            df['close'] = '-'
            df['full_title'] = ''
            df['keywords'] = ''

            save(
              df,
              cache_path
            )

            os.remove(file)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    dumps = sys.argv[1]
    files = onlyfiles = [ os.path.join(dumps, f) for f in os.listdir(dumps) ]

    cache = sys.argv[2]
    parse(files, cache)
