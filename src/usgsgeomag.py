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

plt.style.use(r'./src/my_style')

fig = plt.figure(
    num=1,
    figsize=(10, 20),
    tight_layout=False,
    constrained_layout=True,
)

fig.suptitle("USGS Mag")

ax0 = plt.subplot2grid((2, 2), (0, 0), rowspan=1, colspan=2)
ax1 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((2, 2), (1, 1), rowspan=1, colspan=1)

ax0.plot(
    dst['dtg'],
    dst['dst'],
    lw=0.8,
)
ax0.axhline(y=0)
ax0.set_title("DST")
ax0.set_xlabel("Time (DoY:Hr)")
ax0.set_ylabel("DST (nT)")

if dst['dst'].max() <= 0:
    dstmax = 10
else:
    dstmax = dst['dst'].max() + 1

ax0.set_ylim(
    [
        dst['dst'].min() - 1,
        dstmax,
    ],
)
ax0.yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.2f'))
ax0.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax0.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
ax0.grid(b=True, axis='x', which='Major', lw=0.8)

ax1.scatter(
    bou['dtg'],
    bou['H'],
    s=2,
)

ax1.set_title("H (Bou)")
ax1.set_xlabel("Time (DoY:Hr)")
ax1.set_ylabel("H (nT)")

ax1.set_ylim(
    [
        bou['H'].min() - 1,
        bou['H'].max() + 1,
    ],
)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax1.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
# ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))
ax1.grid(b=True, axis='x', which='Major', lw=0.8)

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)

ax2.scatter(
    frd['dtg'],
    frd['H'],
    s=2,
)

ax2.set_title("H (Frd)")
ax2.set_xlabel("Time (DoY:Hr)")
ax2.set_ylabel("H (nT)")

ax2.set_ylim(
    [
        frd['H'].min() - 1,
        frd['H'].max() + 1,
    ],
)

ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax2.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax2.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
# ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=10))
ax2.grid(b=True, axis='x', which='Major', lw=0.8)

for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(45)

fig.savefig('./web/img/usgsmag.svg')

plt.close(1)
