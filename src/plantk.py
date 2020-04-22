import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import pandas as pd


r = requests.get('https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json')

r.raise_for_status()

datecols = [
    'time_tag',
]

data = pd.read_json(
    r.text
    convert_dates=datecols,
    #orient='records',
)

data = data.drop([0])

data = data.rename(
    columns={
        0: 'time_tag',
        1: 'Kp',
        2: 'Kp_fraction',
        3: 'a_running',
        4: 'station_count',
    }
)

data['Kp_fraction'] = data['Kp_fraction'].astype('float64')

data['time_tag'] = pd.to_datetime(data['time_tag'])

alpha = plt.figure(
    1,
    figsize=(10,10)
)

alpha.suptitle("Plantary K Index")

plt.bar(
    data['time_tag'],
    data['Kp_fraction'],
)

axes = plt.gca()

plt.xlabel("Time")

plt.ylabel("K Index")

axes.set_ylim([0,9])

axes.set_yticks([0,1,2,3,4,5,6,7,8,9])

axes.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
axes.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%d"))

plt.grid(b=True, which='Major', color='black', lw=0.8)

plt.savefig('../web/img/kp.svg')

plt.close(1)
