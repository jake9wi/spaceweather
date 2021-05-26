"""Plot RTSW Mag."""
import pathlib as pl
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import pandas as pd
import funcs

DTG_FMT = "%j:%H"

funcs.check_cwd(pl.Path.cwd())


def get_rtsw_plasma():
    """Get and parse RTSW plasma."""
    url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'
    r = requests.get(url)
    r.raise_for_status()

    datecols = ['time_tag']

    data = pd.read_json(
        r.text,
        convert_dates=datecols,
    )

    data = data.drop([0])

    data = data.rename(
        columns={
            0: "time_tag",
            1: "density",
            2: "speed",
            3: "temperature",
        },
    )

    data['speed'] = data['speed'].astype('float64')
    data['density'] = data['density'].astype('float64')
    data['temperature'] = data['temperature'].astype('float64')
    data['time_tag'] = pd.to_datetime(data['time_tag'])
    return data


def get_rtsw_mag():
    """Get and parse RTSW magnetic data."""
    url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'
    r = requests.get(url)
    r.raise_for_status()

    datecols = ['time_tag']

    data = pd.read_json(
        r.text,
        convert_dates=datecols,
    )

    data = data.drop([0])

    data = data.rename(
        columns={
            0: "time_tag",
            1: "bx_gsm",
            2: "by_gsm",
            3: "bz_gsm",
            4: "lon_gsm",
            5: "lat_gsm",
            6: "bt",
        },
    )

    data['bz_gsm'] = data['bz_gsm'].astype('float64')
    data['bt'] = data['bt'].astype('float64')
    data['time_tag'] = pd.to_datetime(data['time_tag'])
    return data


rtsw_mag = get_rtsw_mag()
rtsw_plasma = get_rtsw_plasma()

ylimit = abs(max(
    [
        abs(rtsw_mag['bz_gsm'].max()),
        abs(rtsw_mag['bz_gsm'].min()),
    ],
))

yrange = [(ylimit + 0.5) * -1, ylimit + 0.5]

#def myplot():
plt.style.use(r'./src/my_style')

fig = plt.figure(
    num=1,
    figsize=(10, 20),
    tight_layout=False,
    constrained_layout=True,
)

fig.suptitle("Real Time Solar Wind")

ax0 = plt.subplot2grid((3, 2), (0, 0), rowspan=1, colspan=2)
ax1 = plt.subplot2grid((3, 2), (1, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((3, 2), (1, 1), rowspan=1, colspan=1)
ax3 = plt.subplot2grid((3, 2), (2, 0), rowspan=1, colspan=1)
ax4 = plt.subplot2grid((3, 2), (2, 1), rowspan=1, colspan=1)

ax0.scatter(
    rtsw_mag['time_tag'],
    rtsw_mag['bz_gsm'],
    s=2,
)

ax0.set_title("Vertical Component (bz_gsm)")
ax0.set_xlabel("Time (DoY:Hr)")
ax0.set_ylabel("nano-Teslas")
ax0.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax0.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
ax0.axhline(y=0)
ax0.set_ylim(yrange)

# for label in ax0.xaxis.get_ticklabels():
#     label.set_rotation(45)

ax1.scatter(
    rtsw_mag['time_tag'],
    rtsw_mag['bt'],
    s=2,
)

ax1.set_title("Field Total")
ax1.set_xlabel("Time (DoY:Hr)")
ax1.set_ylabel("nano-Teslas")
ax1.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))
ax1.axhline(y=0)
ax1.set_ylim(
    (
        0,
        (rtsw_mag['bt'].max() + 0.5),
    ),
)

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)

ax2.scatter(
    rtsw_plasma['time_tag'],
    rtsw_plasma['speed'],
    s=2,
)

ax2.set_title("speed")
ax2.set_xlabel("Time (DoY:Hr)")
ax2.set_ylabel("km/s")
ax2.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax2.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(45)

ax3.scatter(
    rtsw_plasma['time_tag'],
    rtsw_plasma['density'],
    s=2,
)

ax3.set_title("density")
ax3.set_xlabel("Time (DoY:Hr)")
ax3.set_ylabel("1/cm3")
ax3.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax3.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

for label in ax3.xaxis.get_ticklabels():
    label.set_rotation(45)

ax4.scatter(
    rtsw_plasma['time_tag'],
    rtsw_plasma['temperature'],
    s=2,
)

ax4.set_title("temperature")
ax4.set_xlabel("Time (DoY:Hr)")
ax4.set_ylabel("Kelvins")
ax4.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax4.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

for label in ax4.xaxis.get_ticklabels():
    label.set_rotation(45)

fig.savefig('./web/img/rtsw.svg')

plt.close(1)
