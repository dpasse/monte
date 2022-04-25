import re
import os
import requests
import time
import json
import pandas as pd

from bs4 import BeautifulSoup


def parse(jobs_path, cache_path):
    df = pd.read_csv(jobs_path)

    gosbel_json = []
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as reader:
            gosbel_json = json.loads(reader.read())

    not_closed = df[df['close'] == '-']
    for _, row in not_closed.iterrows():
        cat_id = row['cat_id']
        job_id = row['job_id']

        if any(filter(lambda a: a['cat_id'] == cat_id and a['job_id'] == job_id, gosbel_json)):
            print(f'already pulled {cat_id}/{job_id}')
            continue

        response = requests.get(row['url'])
        if response.status_code == 200:
            bs = BeautifulSoup(
                response.content,
                features='html.parser'
            )

            description = bs.select('.ats-description')[0]

            gosbel_json.append({
                'cat_id': cat_id,
                'job_id': job_id,
                'description': re.sub('\s+', ' ', f'<html><body>{description}</body></html>')
            })

            with open(cache_path, 'w') as writer:
                writer.write(
                    json.dumps(gosbel_json, indent=3)
                )

            time.sleep(5)


if __name__ == '__main__':
    parse('./data/disney/jobs.csv', './data/disney/job_descriptions.json')
