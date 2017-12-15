import csv


def text_to_table(path):
    with open(path, 'r') as file_object:
        reader = csv.reader(file_object, delimiter='\t')
        for input_row in reader:
            output_row = ' & '.join(input_row) + r'\\'
            print(output_row)


if __name__ == '__main__':
    input_path = 'stimulus_protocol_table.txt'
    text_to_table(input_path)
