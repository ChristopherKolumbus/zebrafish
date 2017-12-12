import os
import csv

def get_phase_files(path):
    files = os.listdir(path)
    p_files = []
    for file in files:
        if 'phase' in file and 'phases' not in file:
            p_files.append(file)
    return p_files

def get_stimulus_protocol_file(path):
    files = os.listdir(path)
    for file in files:
        if 'StimulusProtocol.txt' in file:
            return file

def get_stimulus_protocol_data_file(path):
    files = os.listdir(path)
    for file in files:
        if 'StimulusProtocolData.txt' in file:
            return file


def combine_all_phase_files(path, p_files):
    p_data = []
    for p_file in p_files:
        split_p_file = p_file.split('_')
        p = ''.join([c for c in split_p_file[-2] if c.isdigit()])
        n = split_p_file[-3]
        with open(os.path.join(path, p_file), 'r') as f:
            p_file_reader = csv.reader(f, delimiter='\t')
            for row in p_file_reader:
                row = [n, p] + row
                p_data.append(row)
    return p_data


def add_stimulus_protocol_info(path, s_p_file, p_data):
    with open(os.path.join(path, s_p_file), 'r') as f:
        s_p_info = list(csv.reader(f, delimiter='\t'))
    for ind in range(len(p_data)):
        p = int(p_data[ind][1])
        p_data[ind] += s_p_info[p - 1]
    return p_data


def add_phase_starts(path, s_p_d_file, p_data):
    with open(os.path.join(path, s_p_d_file), 'r') as f:
        s_p_d_file_reader = csv.reader(f, delimiter='\t')
        current_phase = 1
        phase_starts = []
        for row in s_p_d_file_reader:
            if int(float(row[-1])) == current_phase:
                phase_starts.append(row[0])
                current_phase += 1
    time_offset = float(s_p_d_file.split('_')[-2])
    for ind in range(len(phase_starts)):
        phase_starts[ind] = str(float(phase_starts[ind]) - time_offset)
    for ind in range(len(p_data)):
        p = int(p_data[ind][1])
        p_data[ind].append(phase_starts[p - 1])
    return p_data

'''def add_amplitude(path, s_p_d_file, p_data):
    with open(os.path.join(path, s_p_d_file), 'r') as f:
        s_p_d_file_reader = csv.reader(f, delimiter='\t')
        time = []
        left_trace = []
        right_trace = []
        for row in s_p_d_file_reader:
            time.append(float(row[0]))
            left_trace.append(float(row[4]))
            right_trace.append(float(row[5]))
    time = np.array(time)
    left_trace = np.array(left_trace)
    right_trace = np.array(right_trace)
    for ind in range(len(p_data)):
        left_sacc_time = float(p_data[ind][2])
        print(left_trace[left_trace > left_sacc_time - .5])'''


def get_new_file_name(file_name):
    split_file_name = file_name.split('_')
    split_file_name[-2] = 'all_phases'
    del split_file_name[-3]
    return '_'.join(split_file_name)


def export_phase_data(path, file_name, p_data):
    with open(os.path.join(path, file_name), 'w', newline='') as f:
        output_writer = csv.writer(f, delimiter='\t')
        for row in p_data:
            output_writer.writerow(row)


def main(path):
    phase_files = get_phase_files(input_path)
    stimulus_protocol_file = get_stimulus_protocol_file(input_path)
    stimulus_protocol_data_file = get_stimulus_protocol_data_file(input_path)
    phase_data = combine_all_phase_files(input_path, phase_files)
    phase_data = add_phase_starts(input_path, stimulus_protocol_data_file, phase_data)
    phase_data = add_stimulus_protocol_info(input_path, stimulus_protocol_file, phase_data)
    new_file_name = get_new_file_name(phase_files[0])
    export_phase_data(input_path, new_file_name, phase_data)


if __name__ == '__main__':
    input_path = r'E:\Christoph\Downloads\data_saccades_detected\data_saccades_detected\fish01'
    main(input_path)