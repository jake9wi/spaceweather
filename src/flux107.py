"""Plot the json file containg 10.7cm flux."""
import pathlib as pl
import datetime as dt
import time
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
    if __debug__ == True:
        T0 = time.perf_counter()

    url_obsv = 'https://services.swpc.noaa.gov/json/f107_cm_flux.json'

    robsv = requests.get(url_obsv)
    robsv.raise_for_status()

    if __debug__ == True:
        print("DL:", time.perf_counter() - T0)
        T1 = time.perf_counter()

    date_cols = ['time_tag', 'avg_begin_date']

    data = pd.read_json(
        robsv.text,
        convert_dates=date_cols,
    )

    data = data.loc[data['reporting_schedule'] == 'Noon']

    if __debug__ == True:
        print("Parse:", time.perf_counter() - T1)

    return data


def pred():
    """Get and parse predictions."""
    if __debug__ == True:
        T0 = time.perf_counter()

    url_pred = 'https://services.swpc.noaa.gov/json/predicted_f107cm_flux.json'

    rpred = requests.get(url_pred)
    rpred.raise_for_status()

    if __debug__ == True:
        print("DL:", time.perf_counter() - T0)
        T1 = time.perf_counter()

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

    if __debug__ == True:
        print("Parse:", time.perf_counter() - T1)

    return data

def plot(obsv, pred):
    if __debug__ == True:
        T0 = time.perf_counter()
    plt.style.use(r'./src/my_style')

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
        color='0.75',
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

    if __debug__ == True:
        print("Plot:", time.perf_counter() - T0)

obsv = obsv()
pred = pred()

plot(obsv, pred)
