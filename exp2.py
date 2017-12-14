from auxfuns import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

# load relevant data
data = load_csv_master('all_data01.txt')

fishids = np.unique(data['fishid'])
tfreqs = np.unique(np.abs(data['tempfreq']))  # pool positive and negative stimulus movements
speriods = np.sort(1. / np.unique(data['spatfreq']))  # use spatial period instead of frequency

plt.figure()
plt.subplot(1, 1, 1)
plt.loglog(np.abs(data['degpersec']) * data['spatfreq'], 1. / data['cycper360deg'], '*')


plt.show()


# calculate results
spslope_mean = []

for fidx, fishid in enumerate(fishids):
    fishfilt = data['fishid'] == fishid

    for tidx, tfreq in enumerate(tfreqs):
        tempfilt = np.abs(data['tempfreq']) == tfreq

        for sidx, speriod in enumerate(speriods):
            spatfilt = 1. / data['spatfreq'] == speriod
            filtvec = fishfilt & tempfilt & spatfilt

            rspslope = np.abs(data['rspslope'][filtvec])
            lspslope = np.abs(data['lspslope'][filtvec])

            if len(rspslope) + len(lspslope) > 0:
                mean_spslope = np.nanmean(rspslope) / 2 + np.nanmean(lspslope) / 2
            else:
                mean_spslope = 0

            spslope_mean[tidx, sidx, fidx] = mean_spslope



plt.figure()
ax = plt.subplot()
img = ax.imshow(spslope_mean[:, :, 0], 'viridis', extent=[speriods[0], speriods[-1], tfreqs[0], tfreqs[-1]])

# this ensures the spectrogram fills the plotbox
ax.set_aspect('auto')
ax.autoscale_view(tight=True)
ax.set_autoscale_on(False)
ax.set_xlabel('Spatial period [deg/cyc]')
ax.set_ylabel('Temporal frequency [cyc/deg]')

plt.colorbar(img, ax=ax)
plt.show()

embed()

