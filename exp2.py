from auxfuns import *
from IPython import embed
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle
from scipy.stats import sem
import sys
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


if 'load' in sys.argv:

    # load relevant data
    data = load_csv_master('all_data01.txt')

    print('Calculating fish data...')
    # average for each fish
    sacc_freq = []
    sacc_amp = []
    sacc_permin = []
    slowphase_vel = []
    slowphase_gain = []
    tempfreqs = []
    spatfreqs = []
    for fidx, fishid in enumerate(np.unique(data['fishid'])):
        print(fishid)
        fishfilt = data['fishid'] == fishid

        for tidx, tfreq in enumerate(np.unique(np.abs(data['tempfreq']))):
            tempfilt = np.abs(data['tempfreq']) == tfreq

            for sidx, sfreq in enumerate(np.unique(data['spatfreq'])):
                spatfilt = data['spatfreq'] == sfreq
                filtvec = fishfilt & tempfilt & spatfilt

                if sum(filtvec) > 0:
                    trial_nums = len(np.unique(data['stimphase'][filtvec]))  # number of 60s trials

                    rsaccfreq = sum(np.logical_not(np.isnan(data['rsaccamp'][filtvec]))) / trial_nums  # saccades per minute
                    lsaccfreq = sum(np.logical_not(np.isnan(data['lsaccamp'][filtvec]))) / trial_nums  # saccades per minute
                    rsaccamp = np.abs(data['rsaccamp'][filtvec])
                    lsaccamp = np.abs(data['lsaccamp'][filtvec])
                    rspslope = np.abs(data['rspslope'][filtvec])
                    lspslope = np.abs(data['lspslope'][filtvec])
                    stim_degpersec = tfreq / sfreq

                    # append data
                    tempfreqs.append(tfreq)
                    spatfreqs.append(sfreq)

                    sacc_freq.append(np.mean([lsaccfreq, rsaccfreq]))
                    sacc_amp.append(np.nanmean(np.concatenate((rsaccamp, lsaccamp))))
                    slowphase_vel.append(np.nanmean(np.concatenate((rspslope, lspslope))))
                    slowphase_gain.append(slowphase_vel[-1] / stim_degpersec)

    # convert to array
    sacc_freq = np.asarray(sacc_freq)
    sacc_amp = np.asarray(sacc_amp)
    slowphase_vel = np.asarray(slowphase_vel)
    slowphase_gain = np.asarray(slowphase_gain)
    tempfreqs = np.asarray(tempfreqs)
    spatfreqs = np.asarray(spatfreqs)


    # average over fish
    sacc_freq_avg = []
    sacc_freq_sem = []
    sacc_amp_avg = []
    sacc_amp_sem = []
    slowphase_vel_avg = []
    slowphase_vel_sem = []
    slowphase_gain_avg = []
    slowphase_gain_sem = []
    avg_sfreqs = []
    avg_tfreqs = []
    for idx, (tfreq, sfreq)in enumerate(list(set(list(zip(tempfreqs, spatfreqs))))):  # too complicated to elaborate... works fine
        avg_sfreqs.append(sfreq)
        avg_tfreqs.append(tfreq)

        freqs = sacc_freq[(tempfreqs == tfreq) & (spatfreqs == sfreq)]
        amps = sacc_amp[(tempfreqs == tfreq) & (spatfreqs == sfreq)]
        vels = slowphase_vel[(tempfreqs == tfreq) & (spatfreqs == sfreq)]
        gains = slowphase_gain[(tempfreqs == tfreq) & (spatfreqs == sfreq)]


        sacc_freq_avg.append(np.nanmean(freqs))
        sacc_freq_sem.append(sem(freqs, nan_policy='omit'))

        sacc_amp_avg.append(np.nanmean(amps))
        sacc_amp_sem.append(sem(amps, nan_policy='omit'))

        slowphase_vel_avg.append(np.nanmean(vels))
        slowphase_vel_sem.append(sem(vels, nan_policy='omit'))

        slowphase_gain_avg.append(np.nanmean(gains))
        slowphase_gain_sem.append(sem(gains, nan_policy='omit'))

    avg_sfreqs = np.asarray(avg_sfreqs)
    avg_tfreqs = np.asarray(avg_tfreqs)

    sacc_freq_avg = np.asarray(sacc_freq_avg)
    sacc_freq_sem = np.asarray(sacc_freq_sem)

    sacc_amp_avg = np.asarray(sacc_amp_avg)
    sacc_amp_sem = np.asarray(sacc_amp_sem)

    slowphase_vel_avg = np.asarray(slowphase_vel_avg)
    slowphase_vel_sem = np.asarray(slowphase_vel_sem)

    slowphase_gain_avg = np.asarray(slowphase_gain_avg)
    slowphase_gain_sem = np.asarray(slowphase_gain_sem)

    with open('processedData.p', 'wb') as fObj:
        print('Save pickle')
        pickle.dump([
            avg_sfreqs, 
            avg_tfreqs,
            sacc_freq_avg,
            sacc_freq_sem,
            sacc_amp_avg,
            sacc_amp_sem,
            slowphase_vel_avg,
            slowphase_vel_sem,
            slowphase_gain_avg,
            slowphase_gain_sem
        ],fObj)
        fObj.close()

print('Load pickle')
with open('processedData.p', 'rb') as fObj:
    [avg_sfreqs, 
    avg_tfreqs,
    sacc_freq_avg,
    sacc_freq_sem,
    sacc_amp_avg,
    sacc_amp_sem,
    slowphase_vel_avg,
    slowphase_vel_sem,
    slowphase_gain_avg,
    slowphase_gain_sem]  = pickle.load(fObj)
    fObj.close()

#############
# plot data

####
# heatmap-like
heatmap_size = (12.5, 11.5)


freq_unique = np.unique(sacc_freq_avg)
amp_unique = np.unique(sacc_amp_avg)
vel_unique = np.unique(slowphase_vel_avg)
gain_unique = np.unique(slowphase_gain_avg)

cmap_scheme = 'viridis'
#cmap_scheme = 'jet'
#jetcmap = scio.loadmat('jetforpy.mat')['myColors']
markersize = 21
#slowphase_vel_cmap = jetcmap
#slowphase_gain_cmap = jetcmap
#sacc_amp_cmap = jetcmap


fig10 = custom_fig('Saccade frequency on Temporal / spatial', heatmap_size)
ax10 = fig10.add_subplot(1, 1, 1)
# add colorbar
minval = np.min(np.floor(freq_unique))
maxval = np.ceil(np.max(freq_unique))
zticks = np.arange(minval, maxval + 0.01)
cax = ax10.imshow(np.concatenate((zticks, zticks)).reshape((2, -1)), interpolation='nearest', cmap=cmap_scheme)
cbar = fig10.colorbar(cax, ticks=zticks)
cbar.ax.set_ylabel('Saccade frequency [1/min]')
sacc_freq_cmap = np.asarray(cbar.cmap.colors)
sacc_freq_valmap = np.arange(minval, maxval, (maxval - minval) / sacc_freq_cmap.shape[0])
plt.cla()  # clears imshow plot, but keeps the colorbar

fig11 = custom_fig('Saccade amplitude on Temporal / spatial', heatmap_size)
ax11 = fig11.add_subplot(1, 1, 1)
# add colorbar
minval = np.min(np.floor(amp_unique))
maxval = np.ceil(np.max(amp_unique))
zticks = np.arange(minval, maxval + 0.01)
cax = ax11.imshow(np.concatenate((zticks, zticks)).reshape((2, -1)), interpolation='nearest', cmap=cmap_scheme)
cbar = fig11.colorbar(cax, ticks=zticks)
cbar.ax.set_ylabel('Saccade amplitude [deg]')
sacc_amp_cmap = np.asarray(cbar.cmap.colors)
sacc_amp_valmap = np.arange(minval, maxval, (maxval - minval) / sacc_amp_cmap.shape[0])
plt.cla()  # clears imshow plot, but keeps the colorbar


fig12 = custom_fig('Slowphase velocity on Temporal / spatial', heatmap_size)
ax12 = fig12.add_subplot(1, 1, 1)
# add colorbar
minval = np.min(np.floor(vel_unique))
maxval = np.ceil(np.max(vel_unique))
zticks = np.arange(minval, maxval + 0.01)
cax = ax12.imshow(np.concatenate((zticks, zticks)).reshape((2, -1)), interpolation='nearest', cmap=cmap_scheme)
cbar = fig12.colorbar(cax, ticks=zticks)
cbar.ax.set_ylabel('Slowphase velocity [deg/s]')
slowphase_vel_cmap = np.asarray(cbar.cmap.colors)
slowphase_vel_valmap = np.arange(minval, maxval, (maxval - minval) / slowphase_vel_cmap.shape[0])
plt.cla()  # clears imshow plot, but keeps the colorbar

fig13 = custom_fig('Slowphase gain on Temporal / spatial', heatmap_size)
ax13 = fig13.add_subplot(1, 1, 1)
# add colorbar
minval = np.floor(np.min(gain_unique) * 10) / 10
maxval = np.ceil(np.max(gain_unique) * 10) / 10
zticks = np.arange(minval, maxval + 0.01, 0.1)
cax = ax13.imshow(np.concatenate((zticks, zticks)).reshape((2, -1)), interpolation='nearest', cmap=cmap_scheme)
cbar = fig13.colorbar(cax, ticks=zticks)
cbar.ax.set_ylabel('Slowphase gain')
slowphase_gain_cmap = np.asarray(cbar.cmap.colors)
slowphase_gain_valmap = np.arange(minval, maxval, (maxval - minval) / slowphase_gain_cmap.shape[0])
plt.cla()  # clears imshow plot, but keeps the colorbar

def plot_colorpoint(ax, x, y, z, cmap, valmap, fontsize = 9):
    if sum(z < valmap) > len(valmap) / 2:
        fontcolor = 'w'
    else:
        fontcolor = 'k'
    ax.loglog(x, y, marker='o', markersize=markersize, color=cmap[np.argmin(np.abs(valmap - z)), :])
    ax.text(x, y, str(round(z, 1)), fontsize=fontsize, color=fontcolor,  ha='center', va='center')

for sfreq, tfreq, freq, amp, vel, gain in zip(avg_sfreqs, avg_tfreqs, sacc_freq_avg, sacc_amp_avg, slowphase_vel_avg, slowphase_gain_avg):
    plot_colorpoint(ax10, sfreq, tfreq, freq, sacc_freq_cmap, sacc_freq_valmap)
    plot_colorpoint(ax11, sfreq, tfreq, amp, sacc_amp_cmap, sacc_amp_valmap)
    plot_colorpoint(ax12, sfreq, tfreq, vel, slowphase_vel_cmap, slowphase_vel_valmap)
    plot_colorpoint(ax13, sfreq, tfreq, gain, slowphase_gain_cmap, slowphase_gain_valmap)


def set_axes(ax, xlim = [0.01, 0.3], ylim = [0.1, 5]):
    ax.set_xlabel('Spatial frequency [cyc/deg]')
    ax.set_ylabel('Temporal frequency [cyc/s]')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    adjust_spines(ax)

# adjust axes
set_axes(ax10)
set_axes(ax11)
set_axes(ax12)
set_axes(ax13)

fig10.savefig('../sacc_freq_map.svg', format='svg')

fig11.savefig('../sacc_amp_map.svg', format='svg')

fig12.savefig('../slowphase_vel_map.svg', format='svg')

fig13.savefig('../slowphase_gain_map.svg', format='svg')



mpl.rcParams['figure.subplot.top'] = 0.98
mpl.rcParams['figure.subplot.bottom'] = 0.07
mpl.rcParams['figure.subplot.left'] = 0.08
mpl.rcParams['figure.subplot.right'] = 0.97
mpl.rcParams['figure.subplot.wspace'] = 0.15


################################################################
#### ISO PLOTS (APPENDIX)


isoPlotSize = cm2inch(20, 20)
plotFormat = dict(color='black')
ax = list()

################################
### ISO TF

figIsoTF, axIsoTF = plt.subplots(nrows=4, ncols=2, num='ISO TF', figsize=isoPlotSize)
ax.append(axIsoTF)
const = np.round(avg_tfreqs, 1) == 0.8

x0 = avg_sfreqs[const]
x1 = avg_tfreqs[const] / avg_sfreqs[const]

## SACC FREQ
y = sacc_freq_avg[const]
err = sacc_freq_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][0,0].semilogx()
ax[-1][0,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][0,1].semilogx()
ax[-1][0,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SACC AMP
y = sacc_amp_avg[const]
err = sacc_amp_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][1,0].semilogx()
ax[-1][1,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][1,1].semilogx()
ax[-1][1,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SLOWPHASE VEL
y = slowphase_vel_avg[const]
err = slowphase_vel_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][2,0].semilogx()
ax[-1][2,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][2,1].semilogx()
ax[-1][2,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SLOWPHASE GAIN
y = slowphase_gain_avg[const]
err = slowphase_gain_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][3,0].semilogx()
ax[-1][3,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][3,1].semilogx()
ax[-1][3,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

ax[-1][3,0].set_xlabel('Spatial frequency [1/s]')
ax[-1][3,1].set_xlabel('Velocity [deg/s]')


################################
### ISO SF

figIsoSF, axIsoSF = plt.subplots(nrows=4, ncols=2, num='ISO SF', figsize=isoPlotSize)
ax.append(axIsoSF)
const = np.round(avg_sfreqs, 2) == 0.06

x0 = avg_tfreqs[const]
x1 = avg_tfreqs[const] / avg_sfreqs[const]

## SACC FREQ
y = sacc_freq_avg[const]
err = sacc_freq_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][0,0].semilogx()
ax[-1][0,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][0,1].semilogx()
ax[-1][0,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SACC AMP
y = sacc_amp_avg[const]
err = sacc_amp_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][1,0].semilogx()
ax[-1][1,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][1,1].semilogx()
ax[-1][1,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SLOWPHASE VEL
y = slowphase_vel_avg[const]
err = slowphase_vel_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][2,0].semilogx()
ax[-1][2,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][2,1].semilogx()
ax[-1][2,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SLOWPHASE GAIN
y = slowphase_gain_avg[const]
err = slowphase_gain_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][3,0].semilogx()
ax[-1][3,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][3,1].semilogx()
ax[-1][3,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

ax[-1][3,0].set_xlabel('Temporal frequency [1/s]')
ax[-1][3,1].set_xlabel('Velocity [deg/s]')


################################
### ISO V

figIsoV, axIsoV = plt.subplots(nrows=4, ncols=2, num='ISO V', figsize=isoPlotSize)
ax.append(axIsoV)
const = np.round(avg_sfreqs / avg_tfreqs, 2) == 0.08

x0 = avg_tfreqs[const]
x1 = avg_sfreqs[const]

## SACC FREQ
y = sacc_freq_avg[const]
err = sacc_freq_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][0,0].semilogx()
ax[-1][0,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][0,1].semilogx()
ax[-1][0,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SACC AMP
y = sacc_amp_avg[const]
err = sacc_amp_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][1,0].semilogx()
ax[-1][1,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][1,1].semilogx()
ax[-1][1,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SLOWPHASE VEL
y = slowphase_vel_avg[const]
err = slowphase_vel_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][2,0].semilogx()
ax[-1][2,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][2,1].semilogx()
ax[-1][2,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

## SLOWPHASE GAIN
y = slowphase_gain_avg[const]
err = slowphase_gain_sem[const]
# vs SF
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x0, y, err))))
ax[-1][3,0].semilogx()
ax[-1][3,0].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)
# vs V
xSorted, ySorted, errSorted = list(zip(*sorted(zip(x1, y, err))))
ax[-1][3,1].semilogx()
ax[-1][3,1].errorbar(xSorted, ySorted, yerr=errSorted, **plotFormat)

ax[-1][3,0].set_xlabel('Temporal frequency [1/s]')
ax[-1][3,1].set_xlabel('Spatial frequency [1/deg]')


for a in ax:
    for i,b in enumerate(a[0,:]):
        if i % 2 == 0:
            b.set_ylabel('Frequency [1/min]')
        else:
            b.set_yticklabels([])
        b.set_ylim(2,12)
    for i,b in enumerate(a[1,:]):
        if i % 2 == 0:
            b.set_ylabel('Amplitude [deg]')
        else:
            b.set_yticklabels([])
        b.set_ylim(10,20)
    for i,b in enumerate(a[2,:]):
        if i % 2 == 0:
            b.set_ylabel('Velocity [deg/s]')
        else:
            b.set_yticklabels([])
        b.set_ylim(0,8)
    for i,b in enumerate(a[3,:]):
        if i % 2 == 0:
            b.set_ylabel('Gain')
        else:
            b.set_yticklabels([])
        b.set_ylim(0,0.6)

for a in ax:
    for b in a:
        for c in b:
            adjust_spines(c)


figIsoTF.savefig('../apxIsoTF.svg', format='svg')
figIsoSF.savefig('../apxIsoSF.svg', format='svg')
figIsoV.savefig('../apxIsoV.svg', format='svg')


plt.show()

