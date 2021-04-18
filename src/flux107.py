"""Plot the json file containg 10.7cm flux."""
import pathlib as pl
import datetime as dt
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import pandas as pd
import funcs

DTG_FMT = "%j"

funcs.check_cwd(pl.Path.cwd())


def obsv():
    """Get and parse observations."""
    url_obsv = 'https://services.swpc.noaa.gov/json/f107_cm_flux.json'

    robsv = requests.get(url_obsv)
    robsv.raise_for_status()

    date_cols = ['time_tag']

    data = pd.read_json(
        robsv.text,
        convert_dates=date_cols,
    )

    return data.loc[data['reporting_schedule'] == 'Noon']


def pred():
    """Get and parse predictions."""
    url_pred = 'https://services.swpc.noaa.gov/json/predicted_f107cm_flux.json'

    rpred = requests.get(url_pred)
    rpred.raise_for_status()

    pred_raw = pd.read_json(rpred.text)

    pred_dict = {
        'dtg': [
            pred_raw.iloc[0, 0] + dt.timedelta(days=1),
            pred_raw.iloc[0, 0] + dt.timedelta(days=2),
            pred_raw.iloc[0, 0] + dt.timedelta(days=3),
        ],
        'value': [
            pred_raw.iloc[0, 1],
            pred_raw.iloc[0, 2],
            pred_raw.iloc[0, 3],
        ],
    }

    data = pd.DataFrame(pred_dict)

    return data


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

ax.set_xlabel("Time (DoY)")
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

ax.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

ax.legend()

fig.savefig('./web/img/flux107.svg')

plt.close(1)
