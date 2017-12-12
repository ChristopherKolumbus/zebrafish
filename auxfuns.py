import csv
from IPython import embed
import numpy as np
import os

analysis_path = ['..', 'exp2' ,'data_saccades_detected']

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
        labels = ['lt', 'rt', 'l_sp', 'r_sp', 'stimphase', 'analysis_id', 'fishid']

    return load_csv(filename, labels)



if __name__ == '__main__':
    data = load_csv_master('all_data.txt')

    embed()