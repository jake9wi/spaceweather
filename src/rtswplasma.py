"""Plot rtsw plasma."""
import matplotlib
matplotlib.use('cairo')

import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
import requests
import pandas as pd

url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'
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
        1: "density",
        2: "speed",
        3: "temperature",
    },
)

data['speed'] = data['speed'].astype('float64')
data['density'] = data['density'].astype('float64')
data['temperature'] = data['temperature'].astype('float64')

data['time_tag'] = pd.to_datetime(data['time_tag'])

# # #

plt.style.use('dark_background')

fig, ax = plt.subplots(
    3, 1,
    figsize=(10, 30),
)

# # #

fig.suptitle("Real Time Solar Wind - Plasma")

# # #

ax[0].scatter(
    data['time_tag'],
    data['speed'],
    s=2,
)

ax[0].set_title("speed")
ax[0].set_xlabel("Time")
ax[0].set_ylabel("km/s")

# # #

ax[1].scatter(
    data['time_tag'],
    data['density'],
    s=2,
)

ax[1].set_title("density")
ax[1].set_xlabel("Time")
ax[1].set_ylabel("1/cm3")

# # #

ax[2].scatter(
    data['time_tag'],
    data['temperature'],
    s=2,
)

ax[2].set_title("temperature")
ax[2].set_xlabel("Time")
ax[2].set_ylabel("Kelvins")

# # #

fig.savefig('../web/img/rtsw-plasma.svg')

plt.close(1)

# axes.set_yticks([0,1,2,3,4,5,6,7,8,9])
# axes.xaxis.set_major_formatter(mdates.DateFormatter("%b-%d"))
# axes.xaxis.set_minor_formatter(mdates.DateFormatter("%b-%d"))
