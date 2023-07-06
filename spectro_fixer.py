import re
import os

file_pattern = r'raw(\d+)\.csv'  # Updated pattern to match files like raw*.csv

data_folder = 'data'  # Folder path containing the files

# Get a list of files matching the pattern in the data folder
file_list = [filename for filename in os.listdir(data_folder) if re.match(file_pattern, filename)]

for file_name in file_list:
    with open(os.path.join(data_folder, file_name), 'r') as f:
        # read the first line - the header
        header = f.readline()

        # read the rest of the lines
        lines = f.readlines()

    # apply regex to header
    new_header = re.sub(r'(\d{3}),(\d{2})', r'\1.\2', header)

    # rename first column to 'sample_id'
    new_header = 'sample_id,' + new_header.split(',', 1)[1]

    # get the last digit from the input file name
    match = re.search(r'\d+', file_name)
    last_digit = match.group() if match else None

    # replace entries in the first column with 'sample*' if last_digit exists
    if last_digit:
        for i in range(len(lines)):
            line_values = lines[i].split(',')
            line_values[0] = f'sample{last_digit}'
            lines[i] = ','.join(line_values)

    # Create the output file name by adding '_fixed' before the extension
    output_file = os.path.join(data_folder, file_name.replace('.csv', '_fixed.csv'))

    with open(output_file, 'w') as f:
        f.write(new_header)
        for line in lines:
            f.write(line)
