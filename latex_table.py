import csv


def main(path):
    with open(path, 'r') as file:
        file_reader = csv.reader(file, delimiter='\t')
        for phase, row in enumerate(file_reader):
            phase += 1
            if row[0].startswith('-'):
                direction = 'CCW'
            else:
                direction = 'CW'
            speed = abs(float(row[0]))
            spatial_frequency = float(row[-1]) / 360
            temporal_frequency = abs(float(spatial_frequency * speed))
            duration = row[1][0:2]
            print(rf'{phase} & {speed:.3f} & {spatial_frequency:.3f} & {temporal_frequency:.3f} & {direction} & {duration}\\')


if __name__ == '__main__':
    input_path = r'stimulus_protocol.txt'
    main(input_path)