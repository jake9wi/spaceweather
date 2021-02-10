"""Plot the json file containg 10.7cm flux."""
import matplotlib
matplotlib.use('cairo')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import pandas as pd
import datetime as dt


def obsv():
    robsv = requests.get(
        'https://services.swpc.noaa.gov/json/f107_cm_flux.json'
    )

    robsv.raise_for_status()

    datecols = [
        'time_tag',
    ]

    obsv = pd.read_json(
        robsv.text,
        convert_dates=datecols,
    )

    return obsv.loc[obsv['reporting_schedule'] == 'Noon']


def pred():
    rpred = requests.get(
        'https://services.swpc.noaa.gov/json/predicted_f107cm_flux.json'
    )

    rpred.raise_for_status()

    PredRaw = pd.read_json(
        rpred.text,
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

    return pred

obsv = obsv()
pred = pred()

###

plt.style.use('dark_background')

fig = plt.figure(
    1,
    figsize=(10, 10),
)

fig.suptitle("10.7 centimetre Flux\nSamp Rate: 3x (midday)")

ax = plt.gca()

ax.step(
    obsv['time_tag'],
    obsv['ninety_day_mean'],
    zorder=3,
    label='ninety_day_mean',
    color='green',
)

ax.bar(
    obsv['time_tag'],
    obsv['flux'],
    label='Observed',
    zorder=2,
    lw=0,
    width=0.5,
)

ax.bar(
    pred['dtg'],
    pred['value'],
    color='red',
    label='Predicted',
    zorder=1,
    linewidth=0,
    width=0.5,
)

ax.set_xlabel("Time (UT?)")
ax.set_ylabel("Solar Flux Units (sfu)")

ax.set_ylim(
    [
        min([
            obsv['flux'].min(),
            obsv['ninety_day_mean'].min(),
            pred['value'].min(),
        ]) - 1,

        max([
            obsv['flux'].max(),
            obsv['ninety_day_mean'].max(),
            pred['value'].max(),
        ]) + 1,
    ],
)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%d"))

ax.legend()

fig.savefig('../web/img/flux107.svg')

plt.close(1)
