import sys
import time
import requests
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup


def get_req_number(url):
    print('requesting data from:', url)

    response = requests.get(url)
    if response.status_code == '404':
        return '404 - Not Found'

    bs = BeautifulSoup(
        response.content,
        features='html.parser'
    )

    return bs.select('#jobs-id-scrape')[0].text.strip()

def parse(file_path):
    df = pd.read_csv(file_path)
    df['req_id'] = df['req_id'].fillna('').astype(str)

    for index, row in df[df['req_id'] == ''].iterrows():
        df.loc[df.index == index, 'req_id'] = get_req_number(row['url'])

        print(' * sleeping...')
        print()

        time.sleep(10)

    ## check to see if the 'job_id' changed... but the 'req_id' is still active... which would be a duplicate record.
    df_counts = df.groupby(['req_id']).count()[['cat_id']]
    df_counts.columns = ['count']
    df_counts = df_counts[df_counts['count'] > 1]

    df = df[
        np.logical_or(
            ~df.req_id.isin(df_counts.index),
            np.logical_and(
                df.req_id.isin(df_counts.index),
                df.close == '-'
            )
        )
    ]

    df.to_csv(file_path, index=False)


if __name__ == '__main__':
    file_path = sys.argv[1]

    parse(file_path)
