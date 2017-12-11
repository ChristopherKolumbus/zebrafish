import os
import csv


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


def main(input_path):
    for foldername in os.listdir(input_path):
        print('Folder', foldername)

        input_folder = os.path.join(input_path, foldername)
        # Find text files, ignoring text files containing meta data:
        files = [filename for filename in os.listdir(input_folder) if 'phase' in filename]
        # Create new filename for output file:
        new_filename = create_new_filename(files[0])
        # Skip folder if output file already exists:
        if os.path.isfile(os.path.join(input_folder, new_filename)):
            print('Output file already exists!')
            continue
        # Open output file and create csv writer for output:
        with open(os.path.join(input_folder, new_filename), 'w', newline='') as output_file:
            output_writer = csv.writer(output_file, delimiter='\t')
            # Iterate over all individual text files:
            for filename in files:
                # Get phase and analysis number for current file:
                number, phase = get_number_and_phase(filename)
                # Open current file and create csv reader for input:
                with open(os.path.join(input_folder, filename)) as input_file:
                    input_reader = csv.reader(input_file, delimiter='\t')
                    # Iterate over all rows of input file:
                    for row in input_reader:
                        # Append phase and analysis number to current row:
                        row.extend((phase, number))
                        # Write current row to output file:
                        output_writer.writerow(row)


if __name__ == '__main__':

    input_path = os.path.join(*['..', 'exp2' ,'data_saccades_detected'])
    main(input_path)