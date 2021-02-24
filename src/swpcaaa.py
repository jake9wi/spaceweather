"""Plot USGS geomag data."""
import matplotlib
matplotlib.use('cairo')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import requests
import pandas as pd
import pathlib as pl
import datetime as dt

delta = dt.timedelta(days=1)

dtgfmt = "%j"

def getAAA():
    """Retirve DST data."""
    r = requests.get(
        'https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt'
    )

    r.raise_for_status()

    dgdtmp = pl.Path("../tmp/dgd.txt")

    dgdtmp.write_text(r.text)

    wd = [
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

    data = pd.read_fwf(
        "../tmp/dgd.txt",
        colspecs=wd,
        header=None,
        names=colnames,
        skiprows=13,
        na_values='-1',
        parse_dates=[0],
    )

    return data

def getPRED():
    """Retirve DST data."""
    r = requests.get(
        'https://services.swpc.noaa.gov/json/predicted_fredericksburg_a_index.json'
    )

    r.raise_for_status()

    raw = pd.read_json(
        r.text
    )

    predict = {
        'dtg': [
            raw.iloc[0,0] + dt.timedelta(days=1),
            raw.iloc[0,0] + dt.timedelta(days=2),
            raw.iloc[0,0] + dt.timedelta(days=3),
        ],
        'value':[
            raw.iloc[0,1],
            raw.iloc[0,2],
            raw.iloc[0,3],
        ],
    }

    data = pd.DataFrame(predict)

    return data


aaa = getAAA()
pred = getPRED()

###

plt.style.use('dark_background')

fig, ax = plt.subplots(
    3, 1,
    figsize=(10, 30),
)

fig.suptitle("SWPC A Index")

ax[0].bar(
    aaa['dtg'],
    aaa['A Planet'],
)

ax[0].set_title("Planet (Est)")
ax[0].set_xlabel("Time (DoY)")
ax[0].set_ylabel("A")

ax[0].set_ylim(
    [
        -1,
        101,
    ],
)

ax[0].set_xlim(
    [
        aaa['dtg'].min() - delta,
        pred['dtg'].max() + delta,
    ],
)


ax[0].set_yticks([0, 20, 30, 40, 50, 100], minor=False)
ax[0].set_yticks([10, 60, 70, 80, 90], minor=True)
ax[0].grid(b=True, which='Major', axis='y', color='red', lw=0.8)
ax[0].grid(b=True, which='Minor', axis='y', color='gray', lw=0.8)
ax[0].tick_params(axis='both', which='both', length=12)
ax[0].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax[0].xaxis.set_major_formatter(mdates.DateFormatter(dtgfmt))
ax[0].xaxis.set_minor_formatter(mdates.DateFormatter(dtgfmt))
# ax[0].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))

ax[1].bar(
    pred['dtg'],
    pred['value'],
    zorder=1,
    color='red',
    label='Prediction',
)

ax[1].bar(
    aaa['dtg'],
    aaa['A Fred'],
    zorder=2,
    label='Observation',
)

ax[1].set_title("Fredericksburg (Est)")
ax[1].set_xlabel("Time (DoY)")
ax[1].set_ylabel("A")

ax[1].set_ylim(
    [
        -1,
        101,
    ],
)

ax[1].set_xlim(
    [
        aaa['dtg'].min() - delta,
        pred['dtg'].max() + delta,
    ],
)

ax[1].set_yticks([0, 20, 30, 40, 50, 100], minor=False)
ax[1].set_yticks([10, 60, 70, 80, 90], minor=True)
ax[1].grid(b=True, which='Major', axis='y', color='red', lw=0.8)
ax[1].grid(b=True, which='Minor', axis='y', color='gray', lw=0.8)
ax[1].tick_params(axis='both', which='both', length=12)
ax[1].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax[1].xaxis.set_major_formatter(mdates.DateFormatter(dtgfmt))
ax[1].xaxis.set_minor_formatter(mdates.DateFormatter(dtgfmt))
# ax[1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))

ax[1].legend()

ax[2].bar(
    aaa['dtg'],
    aaa['A Coll'],
)

ax[2].set_title("College (Est)")
ax[2].set_xlabel("Time (DoY)")
ax[2].set_ylabel("A")

ax[2].set_ylim(
    [
        -1,
        101,
    ],
)

ax[2].set_xlim(
    [
        aaa['dtg'].min() - delta,
        pred['dtg'].max() + delta,
    ],
)

ax[2].set_yticks([0, 20, 30, 40, 50, 100], minor=False)
ax[2].set_yticks([10, 60, 70, 80, 90], minor=True)
ax[2].grid(b=True, which='Major', axis='y', color='red', lw=0.8)
ax[2].grid(b=True, which='Minor', axis='y', color='gray', lw=0.8)
ax[2].tick_params(axis='both', which='both', length=12)
ax[2].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax[2].xaxis.set_major_formatter(mdates.DateFormatter(dtgfmt))
ax[2].xaxis.set_minor_formatter(mdates.DateFormatter(dtgfmt))
# ax[2].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))


fig.savefig('../web/img/swpcaaa.svg')

plt.close(1)
