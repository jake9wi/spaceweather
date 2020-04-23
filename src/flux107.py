"""Plot the json file containg 10.7cm flux."""
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

###

plt.style.use('dark_background')

fig = plt.figure(
    1,
    figsize=(10, 10),
)

fig.suptitle("10.7 centimetre Flux")

ax = plt.gca()

ax.bar(
    data['time_tag'],
    data['flux'],
)

ax.set_xlabel("Time")
ax.set_ylabel("Solar Flux Units (sfu)")

ax.set_ylim(
    [
        data['flux'].min(),
        data['flux'].max() + 1,
    ],
)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%d"))

fig.savefig('../web/img/flux107.svg')

plt.close(1)
