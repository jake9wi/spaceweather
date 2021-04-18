"""Plot USGS geomag data."""
import pathlib as pl
import datetime as dt
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import requests
import pandas as pd
import funcs

DTG_FMT = '%j:%H'

funcs.check_cwd(pl.Path.cwd())

deltaT = dt.timedelta(hours=73)

now = dt.datetime.utcnow().isoformat(timespec='minutes')
end = (dt.datetime.utcnow() - deltaT).isoformat(timespec='minutes')


def get_dst():
    """Retirve DST data."""
    col_width = [
        (0, 23),
        (24, 27),
        (32, 40),
    ]

    colnames = [
        'dtg',
        'doy',
        'dst',
    ]

    payload = {
        'id': 'USGS',
        'elements': 'UX4',
        'format': 'iaga2002',
        'sampling_period': '60',
        'type': 'variation',
        'endtime': now,
        'starttime': end,
    }

    url = 'https://geomag.usgs.gov/ws/data/'

    r = requests.get(url, params=payload)
    r.raise_for_status()

    tmp = pl.Path('./src/aaa.tmp')
    tmp.write_text(r.text)

    data = pd.read_fwf(
        tmp,
        colspecs=col_width,
        header=None,
        names=colnames,
        skiprows=21,
        na_values='99999.00',
        parse_dates=[0],
    )
    tmp.unlink()
    return data


def get_bou():
    """Retrive H data for Boulder."""
    col_width = [
        (0, 23),
        (24, 27),
        (32, 40),
    ]

    colnames = [
        'dtg',
        'doy',
        'H',
    ]

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

    tmp = pl.Path('./src/aaa.tmp')
    tmp.write_text(r.text)

    data = pd.read_fwf(
        tmp,
        colspecs=col_width,
        header=None,
        names=colnames,
        skiprows=21,
        na_values='99999.00',
        parse_dates=[0],
    )
    tmp.unlink()
    return data


def get_frd():
    """Retrive H data for Fredricksburg."""
    col_width = [
        (0, 23),
        (24, 27),
        (32, 40),
    ]

    colnames = [
        'dtg',
        'doy',
        'H',
    ]

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

    tmp = pl.Path('./src/aaa.tmp')
    tmp.write_text(r.text)

    data = pd.read_fwf(
        tmp,
        colspecs=col_width,
        header=None,
        names=colnames,
        skiprows=21,
        na_values='99999.00',
        parse_dates=[0],
    )
    tmp.unlink()
    return data


dst = get_dst()
bou = get_bou()
frd = get_frd()

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
    lw=0.8,
)
ax[0].axhline(y=0)
ax[0].set_title("DST")
ax[0].set_xlabel("Time (DoY:Hr)")
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
ax[0].xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax[0].xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
# ax[0].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))
ax[0].grid(b=True, axis='x', which='Major', color='gray', lw=0.8)

ax[1].plot(
    bou['dtg'],
    bou['H'],
    lw=0.8,
)

ax[1].set_title("H (Bou)")
ax[1].set_xlabel("Time (DoY:Hr)")
ax[1].set_ylabel("H (nT)")

ax[1].set_ylim(
    [
        bou['H'].min() - 1,
        bou['H'].max() + 1,
    ],
)
ax[1].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax[1].xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax[1].xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
# ax[1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))
ax[1].grid(b=True, axis='x', which='Major', color='gray', lw=0.8)

ax[2].plot(
    frd['dtg'],
    frd['H'],
    lw=0.8,
)

ax[2].set_title("H (Frd)")
ax[2].set_xlabel("Time (DoY:Hr)")
ax[2].set_ylabel("H (nT)")

ax[2].set_ylim(
    [
        frd['H'].min() - 1,
        frd['H'].max() + 1,
    ],
)

ax[2].yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax[2].xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax[2].xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
# ax[2].xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))
ax[2].grid(b=True, axis='x', which='Major', color='gray', lw=0.8)

fig.savefig('./web/img/usgsmag.svg')

plt.close(1)
