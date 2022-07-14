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
    keywords = []
    title = row['full_title']

    senior_expressions = [
        r'\b(senior)\b',
    ]

    if is_a(senior_expressions, title):
        keywords.append('SENIOR')

    principal_expressions = [
        r'\b(principal)\b',
    ]

    if is_a(principal_expressions, title):
        keywords.append('PRINCIPAL')

    associate_expressions = [
        r'\b(associate)\b',
    ]

    if is_a(associate_expressions, title):
        keywords.append('ASSOCIATE')

    ph_expressions = [
        r'(project hire)',
    ]

    if is_a(ph_expressions, title):
        keywords.append('PROJECT-HIRE')

    director_expressions = [
        r'\b(director)\b',
    ]

    if is_a(director_expressions, title):
        keywords.append('DIRECTOR')

    lead_expressions = [
        r'\b(lead)\b',
    ]

    if is_a(lead_expressions, title):
        keywords.append('LEAD')

    manager_expressions = [
        r'\b(manager)\b',
    ]

    if is_a(manager_expressions, title):
        keywords.append('MANAGER')

    return ', '.join(keywords)

def get_job_type(row):
    jobs = []
    title = row['full_title']

    software_expressions = [
        r'\b(software)\b',
    ]

    if is_a(software_expressions, title):
        jobs.append('SOFTWARE')

    mechanical_expressions = [
        r'\b(mechanical)\b',
    ]

    if is_a(mechanical_expressions, title):
        jobs.append('MECHANICAL')

    electrical_expressions = [
        r'\b(electrical)\b',
    ]

    if is_a(electrical_expressions, title):
        jobs.append('ELECTRICAL')

    electronics_expressions = [
        r'\b(electronics?)\b',
    ]

    if is_a(electronics_expressions, title):
        jobs.append('ELECTRONICS')

    structural_expressions = [
        r'\b(structural)\b',
    ]

    if is_a(structural_expressions, title):
        jobs.append('STRUCTURAL')

    research_expressions = [
        r'\b(research)\b',
    ]

    if is_a(research_expressions, title):
        jobs.append('RESEARCH')

    superintendent_expressions = [
        r'\b(superintendent)\b',
    ]

    if is_a(superintendent_expressions, title):
        jobs.append('SUPERINTENDENT')

    product_expressions = [
        r'\b(product)\b'
    ]

    if is_a(product_expressions, title):
        jobs.append('PRODUCT')

    production_expressions = [
        r'\b(production)\b',
    ]

    if is_a(production_expressions, title):
        jobs.append('PRODUCTION')

    systems_expressions = [
        r'\b(systems?)\b',
    ]

    if is_a(systems_expressions, title):
        jobs.append('SYSTEMS')

    estimator_expressions = [
        r'\b(estimator)\b',
    ]

    if is_a(estimator_expressions, title):
        jobs.append('ESTIMATOR')

    planner_expressions = [
        r'\b(planner)\b',
    ]

    if is_a(planner_expressions, title):
        jobs.append('PLANNER')

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
