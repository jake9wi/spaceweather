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

deltaT = dt.timedelta(
    hours=25,
)

now = dt.datetime.utcnow().isoformat(timespec='minutes')
end = (dt.datetime.utcnow() - deltaT).isoformat(timespec='minutes')


def getDST():
    """Retirve DST data."""
    payload = {
        'id': 'USGS',
        'elements': 'UX4',
        'format': 'iaga2002',
        'sampling_period': '60',
        'type': 'variation',
        'endtime': now,
        'starttime': end,
    }
    r = requests.get('https://geomag.usgs.gov/ws/data/', params=payload)

    r.raise_for_status()

    dsttmp = pl.Path("../tmp/dst.txt")

    dsttmp.write_text(r.text)

    wd = [
        (0, 23),
        (24, 27),
        (32, 40),
    ]

    colnames = [
        'dtg',
        'doy',
        'dst',
    ]

    data = pd.read_fwf(
        "../tmp/dst.txt",
        colspecs=wd,
        header=None,
        names=colnames,
        skiprows=21,
        na_values='99999.00',
        parse_dates=[0],
    )

    return data


def getBOU():
    """Retrive H data for Boulder."""
    payload = {
        'id': 'BOU',
        'elements': 'H',
        'format': 'iaga2002',
        'sampling_period': '60',
        'type': 'variation',
        'endtime': now,
        'starttime': end,
    }
    r = requests.get('https://geomag.usgs.gov/ws/data/', params=payload)

    r.raise_for_status()

    boutmp = pl.Path("../tmp/bou.txt")

    boutmp.write_text(r.text)

    wd = [
        (0, 23),
        (24, 27),
        (32, 40),
    ]

    colnames = [
        'dtg',
        'doy',
        'H',
    ]

    data = pd.read_fwf(
        "../tmp/bou.txt",
        colspecs=wd,
        header=None,
        names=colnames,
        skiprows=21,
        na_values='99999.00',
        parse_dates=[0],
    )

    return data


def getFRD():
    """Retrive H data for Fredricksburg."""
    payload = {
        'id': 'FRD',
        'elements': 'H',
        'format': 'iaga2002',
        'sampling_period': '60',
        'type': 'variation',
        'endtime': now,
        'starttime': end,
    }
    r = requests.get('https://geomag.usgs.gov/ws/data/', params=payload)

    r.raise_for_status()

    frdtmp = pl.Path("../tmp/frd.txt")

    frdtmp.write_text(r.text)

    wd = [
        (0, 23),
        (24, 27),
        (32, 40),
    ]

    colnames = [
        'dtg',
        'doy',
        'H',
    ]

    data = pd.read_fwf(
        "../tmp/frd.txt",
        colspecs=wd,
        header=None,
        names=colnames,
        skiprows=21,
        na_values='99999.00',
        parse_dates=[0],
    )

    return data


dst = getDST()
bou = getBOU()
frd = getFRD()

###

plt.style.use('dark_background')

fig, ax = plt.subplots(
    3, 1,
    figsize=(10, 30),
)

fig.suptitle("USGS Mag")

ax[0].plot(
    dst['dtg'],
    dst['dst'],
)
ax[0].axhline(y=0)
ax[0].set_title("DST")
ax[0].set_xlabel("Time")
ax[0].set_ylabel("DST (nT)")

if dst['dst'].max() <= 0:
    dstmax = 10
else:
    dstmax = dst['dst'].max() + 1

ax[0].set_ylim(
    [
        dst['dst'].min() - 1,
        dstmax,
    ],
)
ax[0].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.2f'))
ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%d%H%M"))
ax[0].xaxis.set_minor_formatter(mdates.DateFormatter("%d%H%M"))
# ax[0].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))


ax[1].plot(
    bou['dtg'],
    bou['H'],
)

ax[1].set_title("H (Bou)")
ax[1].set_xlabel("Time")
ax[1].set_ylabel("H (nT)")

ax[1].set_ylim(
    [
        bou['H'].min() - 1,
        bou['H'].max() + 1,
    ],
)
ax[1].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%d%H%M"))
ax[1].xaxis.set_minor_formatter(mdates.DateFormatter("%d%H%M"))
# ax[1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))

ax[2].plot(
    frd['dtg'],
    frd['H'],
)

ax[2].set_title("H (Frd)")
ax[2].set_xlabel("Time")
ax[2].set_ylabel("H (nT)")

ax[2].set_ylim(
    [
        frd['H'].min() - 1,
        frd['H'].max() + 1,
    ],
)

ax[2].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%d%H%M"))
ax[2].xaxis.set_minor_formatter(mdates.DateFormatter("%d%H%M"))
# ax[2].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))

fig.savefig('../web/img/usgsmag.svg')

plt.close(1)
