from auxfuns import *
from combine_data import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.rcParams['figure.subplot.bottom'] = 0.12
mpl.rcParams['figure.subplot.right'] = 0.95
mpl.rcParams['figure.subplot.left'] = 0.15

examplePath = '..'
exampleFile = 'exp2_20171206_nacre_fish12_rec01_200.4_StimulusProtocolData.txt'

time, leftEyePos, rightEyePos, phase = get_traces(examplePath, exampleFile)

time = np.asarray(time)
leftEyePos = np.asarray(leftEyePos)
rightEyePos = np.asarray(rightEyePos)
phase = np.asarray(phase)


rightEyePosP16 = rightEyePos[phase == 16]
rightEyePosP16 = rightEyePosP16 - np.mean(rightEyePosP16)
leftEyePosP16 = leftEyePos[phase == 16]
leftEyePosP16 = leftEyePosP16 - np.mean(leftEyePosP16)
timeP16 = time[phase == 16]
timeP16 = timeP16 - timeP16[0]




fig = custom_fig('Example OKR', (12, 10))

ylim = [-22, 25]
ytick = np.arange(-20, 20.01, 10)

axRight = plt.subplot(2, 1, 1)
axLeft = plt.subplot(2, 1, 2)

saccadeOnsets = np.asarray([5.7, 15.0, 24.0, 36.4, 47.6, 55.9])

## right eye

axRight.plot(timeP16, rightEyePosP16)
# saccade onsets
axRight.plot(saccadeOnsets, 24 * np.ones(saccadeOnsets.shape[0]), 'r*', markersize=3)
# saccade amplitude
saccAmpRight = [-9.8, 10.2]
yRight = np.asarray([saccAmpRight[0], saccAmpRight[0], saccAmpRight[1], saccAmpRight[1]])
tRight = np.asarray([saccadeOnsets[-3], saccadeOnsets[-3] + 1, saccadeOnsets[-3] + 1, saccadeOnsets[-3]]) + 1
axRight.plot(tRight, yRight, 'k')
# slowphase slope
slowphaseAmpRight = [9.0, -8.0]
tRight = np.asarray([saccadeOnsets[1] + 0.2, saccadeOnsets[2] - 0.3])
axRight.plot(tRight, slowphaseAmpRight, 'r-')


## left eye
axLeft.plot(timeP16, leftEyePosP16)
# saccade onsets
axLeft.plot(saccadeOnsets, 24 * np.ones(saccadeOnsets.shape[0]), 'r*', markersize=3)
# saccade amplitude
saccAmpLeft = [-13.3, 16.6]
yLeft = np.asarray([saccAmpLeft[0], saccAmpLeft[0], saccAmpLeft[1], saccAmpLeft[1]])
tLeft= np.asarray([saccadeOnsets[-3], saccadeOnsets[-3] + 1, saccadeOnsets[-3] + 1, saccadeOnsets[-3]]) + 1
axLeft.plot(tLeft, yLeft, 'k')
# slowphase slope
slowphaseAmpLeft = [13.7, -10.5]
tLeft = np.asarray([saccadeOnsets[1] + 0.2, saccadeOnsets[2] - 0.3])
axLeft.plot(tLeft, slowphaseAmpLeft, 'r-')


axRight.set_ylim(ylim)
axRight.set_yticks(ytick)
axRight.set_xticklabels([])
axRight.set_ylabel('Right eye [deg]')
adjust_spines(axRight)

axLeft.set_ylim(ylim)
axLeft.set_yticks(ytick)
axLeft.set_xlabel('Time [s]')
axLeft.set_ylabel('Left eye [deg]')
adjust_spines(axLeft)

plt.savefig('../okr_example.svg', format='svg')

plt.show()