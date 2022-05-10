import sys
import json
import pandas as pd

def merge(search_type = ''):

    prefix = '' if search_type == '' else f'{search_type}_'
    suffix = '' if search_type == '' else f'_{search_type}'

    documents = {}
    with open(f'./data/disney/{prefix}job_descriptions.json', 'r') as reader:
      for document in json.loads(reader.read()):
        cat_id = document['cat_id']
        job_id = document['job_id']

        key = f'{cat_id}_{job_id}'
        documents[key] = document['description']

    def map_row(row):
        cat_id = row['cat_id']
        job_id = row['job_id']
        key = f'{cat_id}_{job_id}'

        return documents[key]

    df = pd.read_csv(f'./data/disney/{prefix}jobs.csv')
    df['html'] = df.apply(map_row, axis=1)

    df = df.to_csv(f'./data/disney/disney_jobs{suffix}.csv', index=False)


if __name__ == '__main__':
    search_type = ''
    if len(sys.argv) == 2:
        search_type = sys.argv[1]

    merge(search_type)
