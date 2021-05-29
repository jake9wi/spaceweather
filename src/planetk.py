"""Plot Kp index."""
import pathlib as pl
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import requests
import pandas as pd
import funcs

DTG_FMT = '%j:%H'

funcs.check_cwd(pl.Path.cwd())


def get_kp():
    """Get and parse Kp."""
    url = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json'

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
            0: 'time_tag',
            1: 'Kp',
            2: 'Kp_fraction',
            3: 'a_running',
            4: 'station_count',
        },
    )

    data['Kp_fraction'] = data['Kp_fraction'].astype('float64')
    data['time_tag'] = pd.to_datetime(data['time_tag'])
    return data


kp = get_kp()

###

plt.style.use(r'./src/my_style')

fig = plt.figure(
    num=1,
    figsize=(10, 20),
    tight_layout=False,
    constrained_layout=True,
)

fig.suptitle("Plantary K Index")

ax = plt.subplot2grid((2, 1), (0, 0), rowspan=1, colspan=1)
ax1 = plt.subplot2grid((2, 1), (1, 0), rowspan=1, colspan=1)

ax.bar(
    kp['time_tag'],
    kp['Kp_fraction'],
    lw=0,
    width=0.075,
)


ax.axhline(y=9, color='purple', lw=1)  # Class G5
ax.axhline(y=8, color='purple', lw=1)  # Class G4
ax.axhline(y=7, color='purple', lw=1)  # Class G3
ax.axhline(y=6, color='purple', lw=1)  # Class G2
ax.axhline(y=5, color='purple', lw=1)  # Class G1

ax.annotate(
    "G5",
    (0, 0.97),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="purple",
    color="white",
)

ax.annotate(
    "G4",
    (0, 0.86),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="purple",
    color="white",
)

ax.annotate(
    "G3",
    (0, 0.76),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="purple",
    color="white",
)

ax.annotate(
    "G2",
    (0, 0.65),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="purple",
    color="white",
)

ax.annotate(
    "G1",
    (0, 0.55),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="purple",
    color="white",
)

ax.set_xlabel("Time (DoY:Hr)")
ax.set_ylabel("K Index")

ax.set_ylim([-0.25, 9.25])
ax.set_yticks([0, 3, 4, 5, 7, 9], minor=False)
ax.set_yticks([1, 2, 6, 8], minor=True)
ax.tick_params(axis='both', which='both', length=12)
ax.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

ax.grid(b=True, which='both', lw=0.6)


ax1.bar(
    kp['time_tag'],
    kp['a_running'],
    lw=0,
    width=0.075,
)

ax1.set_ylim([-1, 101])
ax1.set_yticks([0, 20, 30, 40, 50, 100], minor=False)
ax1.set_yticks([10, 60, 70, 80, 90], minor=True)
ax1.grid(b=True, which='Major', axis='y', color='red', lw=0.8)
ax1.grid(b=True, which='Minor', axis='y', lw=0.8)
ax1.tick_params(axis='both', which='both', length=12)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('% 1.0f'))
ax1.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

fig.savefig('./web/img/kp.svg')

plt.close(1)
