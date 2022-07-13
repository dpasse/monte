import re
import sys
import pandas as pd


def replace(expressions, replace_with, text):
    for expression in expressions:
        text = re.sub(expression, replace_with, text, flags=re.IGNORECASE)

    return text

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

    return re.sub(r'[ ]{2,}', ' ', title).strip()


def grab_key_words(row):
    title = row['full_title']

    keywords = []

    is_senior = len(
        re.findall(
            r'\b(senior)\b',
            title,
            flags=re.IGNORECASE
        )
    ) > 0

    if is_senior:
        keywords.append('SENIOR')

    is_principal = len(
        re.findall(
            r'\b(principal)\b',
            title,
            flags=re.IGNORECASE
        )
    ) > 0

    if is_principal:
        keywords.append('PRINCIPAL')

    is_associate = len(
        re.findall(
            r'\b(associate)\b',
            title,
            flags=re.IGNORECASE
        )
    ) > 0

    if is_associate:
        keywords.append('ASSOCIATE')

    is_ph = len(
        re.findall(
            r'(project hire)',
            title,
            flags=re.IGNORECASE
        )
    ) > 0

    if is_ph:
        keywords.append('PROJECT-HIRE')

    is_research = len(
        re.findall(
            r'(research)',
            title,
            flags=re.IGNORECASE
        )
    ) > 0

    if is_research:
        keywords.append('RESEARCH')

    return ', '.join(keywords)


def transform(file_path):
    df = pd.read_csv(file_path)

    df['full_title'] = df['title'].map(clean_title)
    df['keywords'] = df.apply(grab_key_words, axis=1)

    df.to_csv(file_path, index=False)


if __name__ == '__main__':
    transform(file_path=sys.argv[1])
