"""Plot USGS geomag data."""
import tempfile
import pathlib as pl
import datetime as dt
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import requests
import pandas as pd
import funcs

delta = dt.timedelta(days=1)

DTG_FMT = "%j"

funcs.check_cwd(pl.Path.cwd())


def get_aaa():
    """Retirve DST data."""
    col_width = [
        (0, 10),
        (14, 16),
        (37, 39),
        (60, 62),
    ]

    colnames = [
        'dtg',
        'A Fred',
        'A Coll',
        'A Planet',
    ]

    url_aaa = 'https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt'

    r = requests.get(url_aaa)
    r.raise_for_status()

    tmp = pl.Path('./src/aaa.tmp')
    tmp.write_text(r.text)

    data = pd.read_fwf(
        tmp,
        colspecs=col_width,
        header=None,
        names=colnames,
        skiprows=13,
        na_values='-1',
        parse_dates=[0],
    )
    tmp.unlink()
    return data


def get_pred():
    """Retirve DST data."""
    url_pred = 'https://services.swpc.noaa.gov/json/predicted_fredericksburg_a_index.json'

    r = requests.get(url_pred)
    r.raise_for_status()

    raw = pd.read_json(r.text)

    predict = {
        'dtg': [
            raw.iloc[0, 0] + dt.timedelta(days=1),
            raw.iloc[0, 0] + dt.timedelta(days=2),
            raw.iloc[0, 0] + dt.timedelta(days=3),
        ],
        'value': [
            raw.iloc[0, 1],
            raw.iloc[0, 2],
            raw.iloc[0, 3],
        ],
    }

    data = pd.DataFrame(predict)

    return data


aaa = get_aaa()
pred = get_pred()

###

plt.style.use(r'./src/my_style')

fig = plt.figure(
    num=1,
    figsize=(10, 20),
    tight_layout=False,
    constrained_layout=True,
)

fig.suptitle("SWPC A Index")

ax0 = plt.subplot2grid((3, 1), (0, 0), rowspan=1, colspan=1)
ax1 = plt.subplot2grid((3, 1), (1, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((3, 1), (2, 0), rowspan=1, colspan=1)

ax0.bar(
    aaa['dtg'],
    aaa['A Planet'],
)

ax0.set_title("Planet (Est)")
ax0.set_xlabel("Time (DoY)")
ax0.set_ylabel("A")

ax0.set_ylim(
    [
        -1,
        101,
    ],
)

ax0.set_xlim(
    [
        aaa['dtg'].min() - delta,
        pred['dtg'].max() + delta,
    ],
)


ax0.set_yticks([0, 20, 30, 40, 50, 100], minor=False)
ax0.set_yticks([10, 60, 70, 80, 90], minor=True)
ax0.grid(b=True, which='Major', axis='y', color='red', lw=0.8)
ax0.grid(b=True, which='Minor', axis='y', lw=0.8)
ax0.tick_params(axis='both', which='both', length=12)
ax0.yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax0.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax0.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

ax1.bar(
    pred['dtg'],
    pred['value'],
    zorder=1,
    color='red',
    label='Prediction',
)

ax1.bar(
    aaa['dtg'],
    aaa['A Fred'],
    zorder=2,
    label='Observation',
)

ax1.set_title("Fredericksburg (Est)")
ax1.set_xlabel("Time (DoY)")
ax1.set_ylabel("A")

ax1.set_ylim(
    [
        -1,
        101,
    ],
)

ax1.set_xlim(
    [
        aaa['dtg'].min() - delta,
        pred['dtg'].max() + delta,
    ],
)

ax1.set_yticks([0, 20, 30, 40, 50, 100], minor=False)
ax1.set_yticks([10, 60, 70, 80, 90], minor=True)
ax1.grid(b=True, which='Major', axis='y', color='red', lw=0.8)
ax1.grid(b=True, which='Minor', axis='y', lw=0.8)
ax1.tick_params(axis='both', which='both', length=12)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax1.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
# ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))

ax1.legend()

ax2.bar(
    aaa['dtg'],
    aaa['A Coll'],
)

ax2.set_title("College (Est)")
ax2.set_xlabel("Time (DoY)")
ax2.set_ylabel("A")

ax2.set_ylim(
    [
        -1,
        101,
    ],
)

ax2.set_xlim(
    [
        aaa['dtg'].min() - delta,
        pred['dtg'].max() + delta,
    ],
)

ax2.set_yticks([0, 20, 30, 40, 50, 100], minor=False)
ax2.set_yticks([10, 60, 70, 80, 90], minor=True)
ax2.grid(b=True, which='Major', axis='y', color='red', lw=0.8)
ax2.grid(b=True, which='Minor', axis='y', lw=0.8)
ax2.tick_params(axis='both', which='both', length=12)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax2.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax2.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
# ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))


fig.savefig('./web/img/swpcaaa.svg')

plt.close(1)
