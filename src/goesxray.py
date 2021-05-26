"""Plot Kp index."""
import argparse
import pathlib as pl
import matplotlib; matplotlib.use('cairo')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import pandas as pd
import funcs

DTG_FMT = '%j:%H'
LIM_MAX = 1 * (10**-2)
LIM_MIN = 1 * (10**-9)

funcs.check_cwd(pl.Path.cwd())


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()

group.add_argument("--three", action='store_true',
                   help="Make three day graph.",
                   )

group.add_argument("--seven", action='store_true',
                   help="Make seven day graph.",
                   )

args = parser.parse_args()

if args.three:
    time_span = 3
elif args.seven:
    time_span = 7
else:
    raise Exception('Option three or seven must be present.')


def get_xray(time_span: int):
    """Get and parse xrays."""
    if time_span == 3:
        url = 'https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json'
    elif time_span == 7:
        url = 'https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json'
    else:
        raise ValueError((
            f'Received: time_span {time_span}. '
            'time_span must be 3 or 7.'
        ))

    r = requests.get(url, timeout=6)
    r.raise_for_status()

    date_cols = ['time_tag']

    data = pd.read_json(
        r.text,
        convert_dates=date_cols,
    )

    xrays_long = data.loc[data['energy'] == '0.1-0.8nm']

    xrays_short = data.loc[data['energy'] == '0.05-0.4nm']

    if (len(xrays_long) == 0) or (len(xrays_short) == 0):
        raise Exception("NO ROWS IN TABLES.")

    return xrays_long, xrays_short


xlong, xshort = get_xray(time_span)

###

plt.style.use(r'./src/my_style')

fig = plt.figure(
    1,
    figsize=(10, 20),
    # facecolor="0.2",
)

fig.suptitle("GOES X-Ray Flux")

ax = plt.gca()

ax.plot(
    xlong['time_tag'],
    xlong['flux'],
    lw=1,
    color='black',
    zorder=2,
    label="Obsv: LONG (0.1-0.8nm)"
)

ax.plot(
    xshort['time_tag'],
    xshort['flux'],
    lw=0.7,
    color='white',
    zorder=1,
    label="Obsv: SHORT (0.05-0.4nm)"
)



ax.axhline(y=1e-4, color='purple', lw=1)  # Class X
ax.axhline(y=1e-5, color='red', lw=1)  # Class  M
ax.axhline(y=1e-6, color='blue', lw=1)  # Class C
ax.axhline(y=1e-7, color='green', lw=1)  # Class B

ax.annotate(
    "Class X",
    (0, 0.725),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="purple",
    color="white",
)

ax.annotate(
    "Class M",
    (0, 0.6),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="red",
    color="white",
)

ax.annotate(
    "Class C",
    (0, 0.45),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="blue",
    color="white",
)

ax.annotate(
    "Class B",
    (0, 0.31),
    xycoords="axes fraction",
    xytext=(10,0),
    textcoords="offset points",
    backgroundcolor="green",
    color="white",
)

ax.set_xlabel("Time (DoY:Hr)")
ax.set_ylabel("Watts per Square Metre")

ax.set_ylim([LIM_MIN, LIM_MAX])
ax.set_yscale('log')
ax.tick_params(axis='both', which='both', length=9, labelsize=12)
ax.xaxis.set_major_formatter(mdates.DateFormatter(DTG_FMT))
ax.xaxis.set_minor_formatter(mdates.DateFormatter(DTG_FMT))

ax.grid(b=True, which='both', lw=0.6)
ax.legend(loc='upper left')
fig.savefig('./web/img/xray.svg')

plt.close(1)
