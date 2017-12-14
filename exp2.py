from auxfuns import *
from IPython import embed
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem
from time import sleep

# load relevant data
data = load_csv_master('all_data01.txt')


# calculate results

# average for each fish
slowphase_gain = []
tempfreqs = []
spatfreqs = []
for fidx, fishid in enumerate(np.unique(data['fishid'])):
    fishfilt = data['fishid'] == fishid

    for tidx, tfreq in enumerate(np.unique(np.abs(data['tempfreq']))):
        tempfilt = np.abs(data['tempfreq']) == tfreq

        for sidx, sfreq in enumerate(np.unique(data['spatfreq'])):
            spatfilt = data['spatfreq'] == sfreq
            filtvec = fishfilt & tempfilt & spatfilt

            rspslope = np.abs(data['rspslope'][filtvec])
            lspslope = np.abs(data['lspslope'][filtvec])
            stim_degpersec = tfreq / sfreq

            if len(rspslope) + len(lspslope) > 0:
                slowphase_gain.append(np.nanmean(np.concatenate((rspslope, lspslope))) / stim_degpersec)

                tempfreqs.append(tfreq)
                spatfreqs.append(sfreq)
# convert to array
slowphase_gain = np.asarray(slowphase_gain)
tempfreqs = np.asarray(tempfreqs)
spatfreqs = np.asarray(spatfreqs)


# average over fish
gain_avg = []
gain_sem = []
avg_sfreqs = []
avg_tfreqs = []
for idx, (tfreq, sfreq)in enumerate(list(set(list(zip(tempfreqs, spatfreqs))))):  # too complicated to elaborate... works fine
    avg_sfreqs.append(sfreq)
    avg_tfreqs.append(tfreq)

    gains = slowphase_gain[(tempfreqs == tfreq) & (spatfreqs == sfreq)]

    gain_avg.append(np.nanmean(gains))
    gain_sem.append(sem(gains, nan_policy='omit'))
gain_avg = np.asarray(gain_avg)
gain_sem = np.asarray(gain_sem)
avg_sfreqs = np.asarray(avg_sfreqs)
avg_tfreqs = np.asarray(avg_tfreqs)


# plot data

# heatmap-like
fig1 = plt.figure('Gain on Temporal / spatial')
ax1 = fig1.add_subplot(1, 1, 1)
gain_unique = np.unique(gain_avg)
cmap = plt.get_cmap('viridis', lut=gain_unique.shape[0])
for sfreq, tfreq, gain in zip(avg_sfreqs, avg_tfreqs, gain_avg):
    ax1.loglog(sfreq, tfreq, marker='o', markersize=20, color=cmap.colors[gain_unique == gain][0])

ax1.set_xlabel('Spatial frequency [cyc/deg]')
ax1.set_ylabel('Temporal frequency [cyc/s]')

# function of spatial freq
fig2 = plt.figure('Gain / spatial (tf=0.8)')
# sort data
const_tf = np.round(avg_tfreqs, 1) == 0.8
sfs, gains, sems = list(zip(*sorted(zip(avg_sfreqs[const_tf], gain_avg[const_tf], gain_sem[const_tf]))))

ax2 = fig2.add_subplot(1, 1, 1)
ax2.semilogx()
ax2.errorbar(sfs, gains, yerr=sems)
ax2.set_xlabel('Spatial frequency [cyc/deg]')
ax2.set_ylabel('Gain')


# function of temporal freq
fig2 = plt.figure('Gain / temporal (sf=0.06)')
# sort data
const_sf = np.round(avg_sfreqs, 2) == 0.06
tfs, gains, sems = list(zip(*sorted(zip(avg_tfreqs[const_sf], gain_avg[const_sf], gain_sem[const_sf]))))

ax2 = fig2.add_subplot(1, 1, 1)
ax2.semilogx()
ax2.errorbar(tfs, gains, yerr=sems)
ax2.set_xlabel('Temporal frequency [cyc/s]')
ax2.set_ylabel('Gain')


# (constant velocity) function of spatial freq
fig3 = plt.figure('(const velocity) Gain / spatial')
# sort data
const_v = np.round(avg_sfreqs / avg_tfreqs, 2) == 0.08
sfs, gains, sems = list(zip(*sorted(zip(avg_sfreqs[const_v], gain_avg[const_v], gain_sem[const_v]))))

ax3 = fig3.add_subplot(1, 1, 1)
ax3.semilogx()
ax3.errorbar(sfs, gains, yerr=sems)
ax3.set_xlabel('Spatial frequency [cyc/deg]')
ax3.set_ylabel('Gain')


# (constant velocity) function of temporal freq
fig3 = plt.figure('(const velocity) Gain / temporal')
# sort data
const_v = np.round(avg_sfreqs / avg_tfreqs, 2) == 0.08
tfs, gains, sems = list(zip(*sorted(zip(avg_tfreqs[const_v], gain_avg[const_v], gain_sem[const_v]))))

ax3 = fig3.add_subplot(1, 1, 1)
ax3.semilogx()
ax3.errorbar(tfs, gains, yerr=sems)
ax3.set_xlabel('Temporal frequency [cyc/s]')
ax3.set_ylabel('Gain')

plt.show()
