import os
import csv
from IPython import embed
import time


if __name__ == '__main__':


    input_path = ['..', 'exp2', 'data_saccades_detected']

    output_path = input_path

    # Open output file and create csv writer for output:
    output_file = open(os.path.join(*output_path, 'all_data.txt'), 'w', newline='')
    output_writer = csv.writer(output_file, delimiter='\t')

    for foldername in os.listdir(os.path.join(*input_path)):
        if foldername[-4:] == '.txt' or foldername[0] == '.':
            continue
        print('Folder', foldername)

        input_folder = os.path.join(*input_path, foldername)
        filename = [filename for filename in os.listdir(input_folder) if 'all_phases' in filename]

        # Open current file and create csv reader for input:
        input_file = open(os.path.join(input_folder, filename[0]))
        input_reader = csv.reader(input_file, delimiter='\t')
        # Iterate over all rows of input file:
        for row in input_reader:
            # Append phase and analysis number to current row:
            row.append(foldername)
            # Write current row to output file:
            output_writer.writerow(row)

        # Close input file:
        input_file.close()
    # Close output file:
    output_file.close()
