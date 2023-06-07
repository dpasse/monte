import os

from bb.utils.filesystem import load_data, save_data


if __name__ == '__main__':
    for file in os.listdir('./data/pbps/'):
        data = load_data(f'./data/pbps/{file}')
        for shot in data['shots']:
            extracts = shot['extracts']

            shot['type']['label'] = 'N/A'

            if '1PT' in extracts['info']:
                shot['type']['label'] = '1PT'

            if '2PT' in extracts['info']:
                shot['type']['label'] = '2PT'

            if '3PT' in extracts['info']:
                shot['type']['label'] = '3PT'

            if shot['type']['label'] == 'N/A' and 'distance' in extracts:
                distance = extracts['distance']['value']

                if distance >= 22:
                    shot['type']['label'] = '3PT'

                if distance < 22:
                    shot['type']['label'] = '2PT'

        save_data(
            f'./data/pbps/{file}',
            data
        )
    