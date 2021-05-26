"""Plot Kp index."""
import pathlib as pl
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
    1,
    figsize=(10, 10),
)

fig.suptitle("Plantary K Index")

ax = plt.gca()

ax.bar(
    kp['time_tag'],
    kp['Kp_fraction'],
    lw=0,
    width=0.075,
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

fig.savefig('./web/img/kp.svg')

plt.close(1)
