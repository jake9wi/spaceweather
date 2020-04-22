import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import requests
import pandas as pd

r = requests.get('https://services.swpc.noaa.gov/json/f107_cm_flux.json')

r.raise_for_status()

datecols = [
    'time_tag',
    'avg_begin_date',
]

data = pd.read_json(
    r.text,
    convert_dates=datecols,
)

print(data)

plt.figure(1,figsize=(10,10))

plt.scatter(data['time_tag'], data['flux'])

plt.savefig('../../web/img/flux107.svg')

plt.close(1)
