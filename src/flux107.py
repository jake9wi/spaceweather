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

alpha = plt.figure(
    1,
    figsize=(10,10)
)

alpha.suptitle("10.7 centimetre Flux")

plt.bar(
    data['time_tag'],
    data['flux'],
)

axes = plt.gca()

plt.xlabel("Time")

plt.ylabel("Solar Flux Units (sfu)")

axes.set_ylim(
    [
        data['flux'].min(),
        data['flux'].max() + 1,
    ]
)

axes.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
axes.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%d"))

plt.savefig('../web/img/flux107.svg')

plt.close(1)
