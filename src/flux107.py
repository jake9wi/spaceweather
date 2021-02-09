"""Plot the json file containg 10.7cm flux."""
import matplotlib
matplotlib.use('cairo')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import pandas as pd
import datetime as dt

robsv = requests.get(
    'https://services.swpc.noaa.gov/json/f107_cm_flux.json'
)

rpred = requests.get(
    'https://services.swpc.noaa.gov/json/predicted_f107cm_flux.json'
)

robsv.raise_for_status()
rpred.raise_for_status()

datecols = [
    'time_tag',
    'avg_begin_date',
]

obsv = pd.read_json(
    robsv.text,
    convert_dates=datecols,
)


PredRaw = pd.read_json(
    rpred.text,
    convert_dates=datecols,
)

PredDict = {
    'dtg': [
        PredRaw.iloc[0,0] + dt.timedelta(days=1),
        PredRaw.iloc[0,0] + dt.timedelta(days=2),
        PredRaw.iloc[0,0] + dt.timedelta(days=3),
    ],
    'value':[
        PredRaw.iloc[0,1],
        PredRaw.iloc[0,2],
        PredRaw.iloc[0,3],
    ],
}

pred = pd.DataFrame(PredDict)

###

plt.style.use('dark_background')

fig = plt.figure(
    1,
    figsize=(10, 10),
)

fig.suptitle("10.7 centimetre Flux\nSamp Rate: 3x (midday)")

ax = plt.gca()

ax.bar(
    obsv['time_tag'],
    obsv['flux'],
    label='Observed',
)

ax.bar(
    pred['dtg'],
    pred['value'],
    color='red',
    label='Predicted',
)

ax.set_xlabel("Time (UT?)")
ax.set_ylabel("Solar Flux Units (sfu)")

ax.set_ylim(
    [
        obsv['flux'].min(),
        obsv['flux'].max() + 1,
    ],
)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%d"))

ax.legend()

fig.savefig('../web/img/flux107.svg')

plt.close(1)
