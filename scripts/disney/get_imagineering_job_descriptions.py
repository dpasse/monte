import re
import os
import requests
import time
import json
import pandas as pd

from bs4 import BeautifulSoup


def break_into_sections(html):
    bs = BeautifulSoup(
        html,
        features='html.parser'
    )

    ignore_sections = [
        'Additional Information:',
        'Additional Information',
        'About Walt Disney Imagineering:',
        'About Walt Disney Imagineering',
        'About The Walt Disney Company:',
        'About The Walt Disney Company',
    ]

    job_description_sections = []
    sections = list(map(lambda a: a.text, bs.select('h4')))
    for start, end in zip(sections, [*sections[1:], '-1']):
        if start in ignore_sections:
            continue

        if end != '-1':
            q = f'(<h4>{start}</h4>)(.+?)(<h4>{end}</h4>)'
        else:
            q = f'(<h4>{start}</h4>)(.+)'

        match = re.search(q, html)
        if match == None:
            continue

        match_html = match.group(2)
        match_html = re.sub('<ul>', '\n\n<ul>', match_html)
        match_html = re.sub('</ul>', '</ul>\n\n', match_html)
        match_html = re.sub('<li>', '<li>* ', match_html)
        match_html = re.sub('</li>', '\n</li>', match_html)

        bs2 = BeautifulSoup(
            match_html,
            features='html.parser'
        )

        text = bs2.get_text()
        text = re.sub(r'(\n\n)(\* )([^\n]+)(\n\n)', r'\1\3\n', text)
        job_description_sections.append({
            'section': re.sub(':\s*$', '', start).strip(),
            'text': text.strip()
        })

    return job_description_sections

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
            description = re.sub('\s+', ' ', f'<html><body>{description}</body></html>')

            gosbel_json.append({
                'cat_id': cat_id,
                'job_id': job_id,
                'description': description,
                'sections': break_into_sections(description),
            })

            with open(cache_path, 'w') as writer:
                writer.write(
                    json.dumps(gosbel_json, indent=3)
                )

            time.sleep(5)


if __name__ == '__main__':
    parse('./data/disney/jobs.csv', './data/disney/job_descriptions.json')
