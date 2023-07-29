from typing import Dict

import os
import re
import time
import requests
import datetime

import pandas as pd

from bs4 import BeautifulSoup

RETRY_ON_ERROR = False

def continuous(max_retries=5, timeout_in_secs=3*60):
    def decorator(func):
        def wrapper():
            retry = 0

            while True:
                try:
                    print('running', '@', datetime.datetime.now())

                    func()
                    retry = 0
                except:
                    if retry >= max_retries:
                        raise

                    retry += 1
                
                time.sleep(timeout_in_secs)
                    
        return wrapper
    
    return decorator

def get() -> str:
    response = requests.get(
        'https://www.laughingplace.com/w/p/magic-kingdom-current-wait-times/'
    )

    assert response.status_code == 200
    return response.text

def parse(html: str) -> dict:
    bs = BeautifulSoup(html, features='html.parser')

    rides: Dict[str, str] = {}
    for row in bs.select('table.lp_attraction tr'):
        columns = row.select('td')

        ride_name = columns[0].text
        wait_time = columns[1].text

        rides[ride_name] = re.sub(
            r'(open|closed)',
            '-',
            re.sub(r'\s+minutes', '', wait_time, flags=re.IGNORECASE),
            flags=re.IGNORECASE
        )

    return {
        'last_check': bs.select('#f_lastcheck')[0].text,
        'rides': rides
    }

def to_pandas_dataframe(response: dict) -> pd.DataFrame:
    last_check = response['last_check']

    rides = list(response['rides'].keys())
    data = list(response['rides'].values())

    return pd.DataFrame(
        [
            [datetime.datetime.now()] + [last_check] + data
        ],
        columns=['time'] + ['last_check'] + rides
    )

def save(df_current: pd.DataFrame) -> None:
    def load_data(ride_times_path):
        df = pd.DataFrame()
        if os.path.exists(ride_times_path):
            df = pd.read_csv(ride_times_path)

        return df

    def merge(df, df_current):
        if df.empty:
            df = df_current
        else:
            if len(df[df['last_check'] == df_current['last_check'][0]]) == 0:
                df = pd.concat([df, df_current])

        return df
    
    ride_times_path = './ride_times.csv'

    df = merge(
        load_data(ride_times_path),
        df_current
    )

    df.to_csv(ride_times_path, index=0)

@continuous()
def run():
    save(
        to_pandas_dataframe(
            parse(
                get()
            )
        )
    )

if __name__ == '__main__':
    run()
