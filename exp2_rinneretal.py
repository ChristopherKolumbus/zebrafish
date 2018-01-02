from auxfuns import *
from IPython import embed
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import sem
from time import sleep
import scipy.io as scio

mpl.rcParams['font.size'] = 11.0

mpl.rcParams['axes.linewidth'] = 1.5

# x axis
mpl.rcParams['xtick.major.size'] = 4
mpl.rcParams['xtick.major.width'] = 1.3
mpl.rcParams['xtick.minor.size'] = 2
mpl.rcParams['xtick.minor.width'] = 1.3

# y axis
mpl.rcParams['ytick.major.size'] = 4
mpl.rcParams['ytick.major.width'] = 1.3
mpl.rcParams['ytick.minor.size'] = 2
mpl.rcParams['ytick.minor.width'] = 1.3


mpl.rcParams['figure.subplot.bottom'] = 0.12
mpl.rcParams['figure.subplot.right'] = 0.95


# load relevant data
data = load_csv('dataFromRinnerEtAl2005.txt', labels = ['spatfreq', 'degpersec', 'tempfreq', 'gain'])

#############
# plot data

####
# heatmap-like
heatmap_size = (12.5, 11.5)

cmap_scheme = 'viridis'
markersize = 17


fig = custom_fig('Slowphase gain on Temporal / spatial', heatmap_size)
ax = fig.add_subplot(1, 1, 1)
# add colorbar
minval = np.floor(np.min(data['gain']) * 10) / 10
maxval = np.ceil(np.max(data['gain']) * 10) / 10
zticks = np.arange(minval, maxval + 0.01, 0.1)
cax = ax.imshow(np.concatenate((zticks, zticks)).reshape((2, -1)), interpolation='nearest', cmap=cmap_scheme)
cbar = fig.colorbar(cax, ticks=zticks)
cbar.ax.set_ylabel('Slowphase gain')
cmap = np.asarray(cbar.cmap.colors)
valmap = np.arange(minval, maxval, (maxval - minval) / cmap.shape[0])
plt.cla()  # clears imshow plot, but keeps the colorbar

def plot_colorpoint(ax, x, y, z, cmap, valmap, fontsize = 9):
    if sum(z < valmap) > len(valmap) / 2:
        fontcolor = 'w'
    else:
        fontcolor = 'k'
    ax.loglog(x, y, marker='o', markersize=markersize, color=cmap[np.argmin(np.abs(valmap - z)), :])
    ax.text(x, y, str(round(z, 1)), fontsize=fontsize, color=fontcolor,  ha='center', va='center')

for sfreq, tfreq, gain in zip(data['spatfreq'], data['tempfreq'], data['gain']):
    plot_colorpoint(ax, sfreq, tfreq, gain, cmap, valmap)

xlim = [0.01, 0.3]
ylim = [0.1, 5]

ax.set_xlabel('Spatial frequency [cyc/deg]')
ax.set_ylabel('Temporal frequency [cyc/s]')
ax.set_xlim(xlim)
ax.set_ylim(ylim)
adjust_spines(ax)

fig.savefig('../slowphase_gain_map_rinner.svg', format='svg')


plt.show()