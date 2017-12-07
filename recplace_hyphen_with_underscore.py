import os

input_folder = r'..\..\Documents\zebrafish'
for filename in os.listdir(input_folder):
    print('Renaming {0}'.format(filename))
    new_filename = ''
    for char in filename:
        if char == '-':
            new_filename += '_'
        else:
            new_filename += char
    os.rename(os.path.join(input_folder, filename), os.path.join(input_folder, new_filename))