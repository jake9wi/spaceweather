"""Plot RTSW Mag."""
import matplotlib
matplotlib.use('cairo')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import pandas as pd

dtgfmt = "%j:%H"

url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'
r = requests.get(url)

r.raise_for_status()


datecols = [
    'time_tag',
]

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

ylimit = abs(max(
    [
        abs(data['bz_gsm'].max()),
        abs(data['bz_gsm'].min()),
    ],
))

yrange = [(ylimit + 0.5) * -1, ylimit + 0.5]

# # #

plt.style.use('dark_background')

fig, ax = plt.subplots(
    2, 1,
    figsize=(10, 20),
)

# # #

fig.suptitle("Real Time Solar Wind - Magnetometre")

# # #

ax[0].scatter(
    data['time_tag'],
    data['bz_gsm'],
    s=2,
)

ax[0].set_title("Vertical Component (bz_gsm)")
ax[0].set_xlabel("Time (DoY:Hr)")
ax[0].set_ylabel("nano-Teslas")
ax[0].xaxis.set_major_formatter(mdates.DateFormatter(dtgfmt))
ax[0].xaxis.set_minor_formatter(mdates.DateFormatter(dtgfmt))
ax[0].axhline(y=0)
ax[0].set_ylim(yrange)

# # #

ax[1].scatter(
    data['time_tag'],
    data['bt'],
    s=2,
)

ax[1].set_title("Field Total")
ax[1].set_xlabel("Time (DoY:Hr)")
ax[1].set_ylabel("nano-Teslas")
ax[1].xaxis.set_major_formatter(mdates.DateFormatter(dtgfmt))
ax[1].xaxis.set_minor_formatter(mdates.DateFormatter(dtgfmt))
ax[1].axhline(y=0)
ax[1].set_ylim(
    (
        0,
        (data['bt'].max() + 0.5),
    ),
)



# # #

fig.savefig('../web/img/rtsw-mag.svg')

plt.close(1)

# axes.set_yticks([0,1,2,3,4,5,6,7,8,9])
# axes.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
# axes.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%d"))
