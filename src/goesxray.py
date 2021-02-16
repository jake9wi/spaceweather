"""Plot Kp index."""
import matplotlib
matplotlib.use('cairo')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import requests
import pandas as pd

dtgfmt = '%j:%H'

def getXRAY3d():
    url = 'https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json'
    r = requests.get(url)
    r.raise_for_status()

    datecols = [
        'time_tag',
    ]

    data = pd.read_json(
        r.text,
        convert_dates=datecols,
    )

    # long, short
    return data.loc[data['energy'] == '0.1-0.8nm'], data.loc[data['energy'] == '0.05-0.4nm']


xlong, xshort = getXRAY3d()

###
limmax = 1 * (10**-2)
limmin = 1 * (10**-9)
###

plt.style.use('dark_background')

fig = plt.figure(
    1,
    figsize=(10, 20),
)

fig.suptitle("GOES X-Ray Flux")

ax = plt.gca()

ax.plot(
    xlong['time_tag'],
    xlong['flux'],
    lw=0.7,
    color='red',
    zorder=2,
    label="Obsv: LONG (0.1-0.8nm)"
)

ax.plot(
    xshort['time_tag'],
    xshort['flux'],
    lw=0.7,
    color='blue',
    zorder=1,
    label="Obsv: SHORT (0.05-0.4nm)"
)

ax.axhline(y=1e-4, label='Class X', color='purple', lw=1)
ax.axhline(y=1e-5, label='Class M', color='red', lw=1)
ax.axhline(y=1e-6, label='Class C', color='yellow', lw=1)
ax.axhline(y=1e-7, label='Class B', color='green', lw=1)

ax.set_xlabel("Time (DoY:Hr)")
ax.set_ylabel("Watts per Square Metre")

ax.set_ylim([limmin, limmax])
ax.set_yscale('log')
ax.tick_params(axis='both', which='both', length=9, labelsize=12)
ax.xaxis.set_major_formatter(mdates.DateFormatter(dtgfmt))
ax.xaxis.set_minor_formatter(mdates.DateFormatter(dtgfmt))

ax.grid(b=True, which='both', color='gray', lw=0.6)
ax.legend(loc='upper left')
fig.savefig('../web/img/xray.svg')

plt.close(1)
