import os
import csv
import math
from IPython import embed


def get_phase_files(input_path):
    files = os.listdir(input_path)
    phase_files = []
    for file in files:
        if 'phase' in file and 'phases' not in file:
            phase_files.append(file)
    return phase_files


def get_all_phases_file(input_path):
    files = os.listdir(input_path)
    for file in files:
        if 'all_phases' in file:
            return file

    return False

def get_stimulus_protocol_file(input_path):
    files = os.listdir(input_path)
    for file in files:
        if 'StimulusProtocol.txt' in file:
            return file


def get_stimulus_protocol_data_file(input_path):
    files = os.listdir(input_path)
    for file in files:
        if 'StimulusProtocolData.txt' in file:
            return file


def combine_all_phase_files(input_path, phase_files):
    phase_data = []
    for phase_file in phase_files:
        split_phase_file = phase_file.split('_')
        phase = ''.join([c for c in split_phase_file[-2] if c.isdigit()])
        analysis_number = split_phase_file[-3]
        with open(os.path.join(input_path, phase_file), 'r') as f:
            phase_file_reader = csv.reader(f, delimiter='\t')
            for row in phase_file_reader:
                row = [analysis_number, phase] + row
                phase_data.append(row)
    return phase_data


def add_stimulus_protocol_info(input_path, stimulus_protocol_file, phase_data):
    with open(os.path.join(input_path, stimulus_protocol_file), 'r') as f:
        stimulus_protocol_info = list(csv.reader(f, delimiter='\t'))
    for index in range(len(phase_data)):
        phase = int(phase_data[index][1])
        phase_data[index] += stimulus_protocol_info[phase - 1]
    return phase_data


def add_phase_starts(input_path, stimulus_protocol_data_file, phase_data):
    with open(os.path.join(input_path, stimulus_protocol_data_file), 'r') as f:
        stimulus_protocol_data_file_reader = csv.reader(f, delimiter='\t')
        current_phase = 1
        phase_beginnings = []
        for row in stimulus_protocol_data_file_reader:
            if int(float(row[-1])) == current_phase:
                phase_beginnings.append(row[0])
                current_phase += 1
    time_line_offset = get_time_line_offset(stimulus_protocol_data_file)
    for index in range(len(phase_beginnings)):
        phase_beginnings[index] = str(float(phase_beginnings[index]) - time_line_offset)
    for index in range(len(phase_data)):
        phase = int(phase_data[index][1])
        phase_data[index].append(phase_beginnings[phase - 1])
    return phase_data


def get_time_line_offset(stimulus_protocol_data_file):
    return float(stimulus_protocol_data_file.split('_')[-2])


def add_saccade_amplitudes(time_line, eye_position, phase_data, which_eye='left'):
    if which_eye.lower() == 'left':
        eye = 2
    else:
        eye = 3
    for index in range(len(phase_data)):
        time_of_saccade = float(phase_data[index][eye])
        if math.isnan(time_of_saccade):
            phase_data[index].append('nan')
        else:
            time_line_slice, eye_position_slice = get_trace_slice(time_line, eye_position, time_of_saccade)
            saccade_amplitude = get_saccade_amplitude(eye_position_slice)
            phase_data[index].append(str(saccade_amplitude))
    return phase_data


def get_traces(input_path, stimulus_protocol_data_file):
    with open(os.path.join(input_path, stimulus_protocol_data_file), 'r') as f:
        time_line = []
        left_eye_position = []
        right_eye_position = []
        time_line_offset = get_time_line_offset(stimulus_protocol_data_file)
        stimulus_protocol_data_file_reader = csv.reader(f, delimiter='\t')
        for row in stimulus_protocol_data_file_reader:
            time_line.append(float(row[0]) - time_line_offset)
            left_eye_position.append(float(row[4]))
            right_eye_position.append(float(row[5]))
    return time_line, left_eye_position, right_eye_position


def get_trace_slice(time_line, eye_position, time_of_saccade, window_size=0.5):
    time_line_slice = []
    eye_position_slice = []
    for time, position in zip(time_line, eye_position):
        if time_of_saccade - window_size < time < time_of_saccade + window_size:
            time_line_slice.append(time)
            eye_position_slice.append(position)
    return time_line_slice, eye_position_slice


def get_saccade_amplitude(eye_position_slice):
    return abs(max(eye_position_slice) - min(eye_position_slice))


def get_new_file_name(file_name):
    split_file_name = file_name.split('_')
    split_file_name[-2] = 'all_phases'
    del split_file_name[-3]
    return '_'.join(split_file_name)


def export_phase_data(input_path, file_name, phase_data):
    with open(os.path.join(input_path, file_name), 'w', newline='') as f:
        output_writer = csv.writer(f, delimiter='\t')
        for row in phase_data:
            output_writer.writerow(row)


def main_combine_phases(input_path):
    phase_files = get_phase_files(input_path)
    stimulus_protocol_file = get_stimulus_protocol_file(input_path)
    stimulus_protocol_data_file = get_stimulus_protocol_data_file(input_path)
    phase_data = combine_all_phase_files(input_path, phase_files)
    time_line, left_eye_position, right_eye_position = get_traces(input_path, stimulus_protocol_data_file)
    phase_data = add_saccade_amplitudes(time_line, left_eye_position, phase_data, which_eye='left')
    phase_data = add_saccade_amplitudes(time_line, right_eye_position, phase_data, which_eye='right')
    phase_data = add_phase_starts(input_path, stimulus_protocol_data_file, phase_data)
    phase_data = add_stimulus_protocol_info(input_path, stimulus_protocol_file, phase_data)
    new_file_name = get_new_file_name(phase_files[0])
    export_phase_data(input_path, new_file_name, phase_data)


def main_combine_fishes(input_path, outfilename):

    # open output file
    with open(os.path.join(*input_path, outfilename), 'w', newline='') as outfile:
        outwriter = csv.writer(outfile, delimiter='\t')

        # iterate through all fish-folders
        for foldername in os.listdir(os.path.join(*input_path)):
            if foldername.endswith('.txt') or not foldername.startswith('fish'):
                continue
            print(foldername)

            # open input-file (all_phases)
            all_phases_file = get_all_phases_file(os.path.join(*input_path, foldername))
            with open(os.path.join(*input_path, foldername, all_phases_file), 'r', newline='') as infile:
                inreader = csv.reader(infile, delimiter='\t')
                for row in inreader:
                    # add fishid to row and add row to outfile
                    row.append(foldername)
                    outwriter.writerow(row)
            infile.close()

    outfile.close()


if __name__ == '__main__':
    # All individual phase files, stimulus protocol file and stimulus protocol data file need to be in this folder:
    input_path = ['..', 'exp2', 'data_saccades_detected']

    # Combine individual phase-files for each fish into all_phases-file
    print('Combining phase files...')
    for foldername in os.listdir(os.path.join(*input_path)):
        if foldername.endswith('.txt') or not foldername.startswith('fish'):
            continue
        print(foldername)

        main_combine_phases(os.path.join(*input_path, foldername))

    print('Combine fish files...')
    main_combine_fishes(input_path, 'all_data.txt')