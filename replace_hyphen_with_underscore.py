import os

replaceChars = {
    '-': '_'
}

input_folder = r'..\..\Documents\zebrafish'
for filename in os.listdir(input_folder):
    print('Renaming {0}'.format(filename))
    new_filename = filename
    for search in replaceChars.keys():
        new_filename = new_filename.replace(search, replaceChars[search])

    os.rename(os.path.join(input_folder, filename), os.path.join(input_folder, new_filename))