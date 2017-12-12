import os
import csv


def get_files(path):
    files = os.listdir(path)
    phase_files = []
    for file in files:
        if 'StimulusProtocol' in file and 'StimulusProtocolData' not in file:
            stim_prot = file
        elif 'StimulusProtocolData' in file:
            stim_prot_data = file
        elif 'phase' in file and 'all_phases' not in file:
            phase_files.append(file)
    return stim_prot, stim_prot_data, phase_files


def get_phase_starts(path):
    with open(path) as f:
        r = csv.reader(f, delimiter='\t')
        c_p = 1
        p_s = []
        for row in r:
            if int(float(row[-1])) == c_p:
                p_s.append(row[0])
                c_p += 1
    return p_s


def get_stimulus_protocol(path):
    with open(path) as f:
        return list(csv.reader(f, delimiter='\t'))

def create_new_filename(filename):
    split_filename = filename.split('_')
    split_filename[-2] = 'all_phases'
    del split_filename[-3]
    return '_'.join(split_filename)


def get_number_and_phase(filename):
    split_filename = filename.split('_')
    p = ''.join([c for c in split_filename[-2] if c.isdigit()])
    n = split_filename[-3]
    return n, p


def combine_phase_files(path):
    stimulus_protocol_file_name, stimulus_protocol_data_file_name, phase_file_names = get_files(path)
    stimulus_protocol = get_stimulus_protocol(os.path.join(path, stimulus_protocol_file_name))
    phase_starts = get_phase_starts(os.path.join(path, stimulus_protocol_data_file_name))
    output_filename = create_new_filename(phase_file_names[0])
    with open(os.path.join(path, output_filename), 'w', newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter='\t')
        for phase_file_name in phase_file_names:
            analysis_number, phase = get_number_and_phase(phase_file_name)
            with open(os.path.join(path, phase_file_name)) as input_file:
                input_reader = csv.reader(input_file, delimiter='\t')
                for row in input_reader:
                    row.extend((phase, analysis_number, phase_starts[int(phase) - 1]))
                    row += stimulus_protocol[int(phase) - 1]
                    print(row)
                    output_writer.writerow(row)

input_path = r'C:\Users\chris\data_saccades_detected\fish01'
combine_phase_files(input_path)