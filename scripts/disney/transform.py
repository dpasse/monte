import re
import sys
import pandas as pd


def replace(expressions, replace_with, text):
    for expression in expressions:
        text = re.sub(expression, replace_with, text, flags=re.IGNORECASE)

    return text

def is_a(expressions, text, flags = re.IGNORECASE):
    for expression in expressions:
        response = len(
            re.findall(expression, text, flags)
        ) > 0

        if response:
            return True

    return False

def clean_title(title):
    title = re.sub(r'^(PH)-(.+)', r'\2 (\1)', title)

    title = replace(
        [
            r'\b(sr\.)',
            r'\b(sr)\b'
        ],
        'Senior',
        title,
    )

    title = replace(
        [
            r'\b(mgr\.)',
            r'\b(mgr)\b'
        ],
        'Manager',
        title,
    )

    title = replace(
        [
            r'\b(asst\.)',
            r'\b(asst)\b'
        ],
        'Assistant',
        title,
    )

    title = replace(
        [
            r'\b(dev\.)',
            r'\b(dev)\b'
        ],
        'Developer',
        title,
    )

    title = replace(
        [
            r'\b(princ\.)',
            r'\b(princ)\b'
        ],
        'Principal',
        title,
    )

    title = replace(
        [
            r'\b(ph)\b',
        ],
        'Project Hire',
        title,
    )

    title = replace(
        [
            r'\b(R&D)\b',
        ],
        'Research and Development',
        title,
    )

    title = replace(
        [
            r'\b(SW)\b',
        ],
        'Software',
        title,
    )

    return re.sub(r'[ ]{2,}', ' ', title).strip()

def get_job_level(row):
    types = {
        'SENIOR': [
            r'\b(senior)\b',
        ],
        'PRINCIPAL': [
            r'\b(principal)\b',
        ],
        'ASSOCIATE': [
            r'\b(associate)\b',
        ],
        'PROJECT-HIRE': [
            r'(project hire)',
        ],
        'DIRECTOR': [
            r'\b(director)\b',
        ],
        'LEAD': [
            r'\b(lead)\b',
        ],
        'MANAGER': [
            r'\b(manager)\b',
        ],
    }

    keywords = []
    for label, expressions in types.items():
        if is_a(expressions, row['full_title']):
            keywords.append(label)

    return ', '.join(keywords)

def get_job_type(row):
    types = {
        'SOFTWARE': [
            r'\b(software)\b',
        ],
        'MECHANICAL': [
            r'\b(mechanical)\b',
        ],
        'CIVIL': [
            r'\b(civil)\b',
        ],
        'ELECTRICAL': [
            r'\b(electrical)\b',
        ],
        'ELECTRONICS': [
            r'\b(electronics?)\b',
        ],
        'STRUCTURAL': [
            r'\b(structural)\b',
        ],
        'RESEARCH': [
            r'\b(research)\b',
        ],
        'SUPERINTENDENT': [
            r'\b(superintendent)\b',
        ],
        'PRODUCT': [
            r'\b(product)\b',
        ],
        'PRODUCTION': [
            r'\b(production)\b',
        ],
        'SYSTEMS': [
            r'\b(systems?)\b',
        ],
        'ESTIMATOR': [
            r'\b(estimator)\b',
        ],
        'PLANNER': [
            r'\b(planner)\b',
        ]
    }

    jobs = []
    for label, expressions in types.items():
        if is_a(expressions, row['full_title']):
            jobs.append(label)

    return ', '.join(jobs)

def transform(file_path):
    df = pd.read_csv(file_path)

    df['full_title'] = df['title'].map(clean_title)

    df['level'] = ''
    df['level'] = df.apply(get_job_level, axis=1)

    df['job_type'] = ''
    df['job_type'] = df.apply(get_job_type, axis=1)

    df.to_csv(file_path, index=False)


if __name__ == '__main__':
    transform(file_path=sys.argv[1])
