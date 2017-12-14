import csv
from IPython import embed
import math
import numpy as np
import os

analysis_path = ['..']

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