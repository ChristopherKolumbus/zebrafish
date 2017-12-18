import csv
from IPython import embed
import math
import matplotlib.pyplot as plt
import numpy as np
import os

analysis_path = ['..']


def adjust_spines(ax, spines = ['left','bottom'], shift_pos = False):
    for loc, spine in ax.spines.items():
        if loc in spines:
            if shift_pos:
                spine.set_position(('outward', 10))  # outward by 10 points
            # spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    elif 'right' in spines:
        ax.yaxis.set_ticks_position('right')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])


def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)


def custom_fig(name, size=(9, 8)):
    return plt.figure(name, figsize=cm2inch(size))


def load_csv(filename, labels):
    # create data dictionary
    data = dict()
    for label in labels:
        data[label] = []

    # load input file
    input_file = open(os.path.join(*analysis_path, filename))
    input_reader = csv.reader(input_file, delimiter='\t')
    input_list = list(input_reader)

    # iterate over all rows of file
    for rowidx, row in enumerate(input_list):
        for colidx, label in enumerate(labels):
            try:
                data[label].append(float(row[colidx]))
            except:
                data[label].append(row[colidx])

    # close file
    input_file.close()

    # convert to numpy arrays
    for colidx, label in enumerate(labels):
        data[label] = np.asarray(data[label])

    # return dictionary
    return data


def load_csv_master(filename, labels = None):
    if labels is None:
        labels = ['analysisid',
                  'stimphase',
                  'ltime',
                  'rtime',
                  'lspslope',
                  'rspslope',
                  'lsaccamp',
                  'rsaccamp',
                  'phasestart',
                  'degpersec',
                  'stimdur',
                  'one1',
                  'one2',
                  'one3',
                  'one4',
                  'one5',
                  'cycper360deg',
                  'fishid']

    data = load_csv(filename, labels)
    data['spatfreq'] = data['cycper360deg'] / 360
    data['spatperiod'] = 1. / data['spatfreq']
    data['tempfreq'] = data['spatfreq'] * data['degpersec']

    return data


if __name__ == '__main__':
    pass