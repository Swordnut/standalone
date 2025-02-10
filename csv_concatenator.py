import csv
import os

folder_path = input("enter the folder where the CSV files are stored")
output_filename = "{folder_path}_merged.csv"

# Get a list of the filenames in the order you specified
filenames = [f'{folder_path}/{i}.csv' for i in range(1, 7)]

# Check for file existence and notify if not found
for idx, filename in enumerate(filenames):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        continue

# Create or overwrite the output file
with open(output_filename, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    for idx, filename in enumerate(filenames):
        with open(filename, 'r', newline='') as infile:
            reader = csv.reader(infile)
            
            # If it's the first file, write headers and all rows
            if idx == 0:
                for row in reader:
                    writer.writerow(row)
            else:
                # For subsequent files, skip the header row
                next(reader)
                for row in reader:
                    writer.writerow(row)

print(f'All CSV files have been concatenated into {output_filename}')

