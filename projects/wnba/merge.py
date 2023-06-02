import os
import json

from bb.utils.filesystem import save_data


if __name__ == '__main__':
    shots = []
    for file in os.listdir('./data/pbps/'):
        with open(f'./data/pbps/{file}', 'r') as json_data:
            data = json.loads(json_data.read())

        shots.extend(data['shots'])

    save_data(
        './data/shots.json',
        shots
    )
