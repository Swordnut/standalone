import csv
import os
import re
from docx import Document
from concurrent.futures import ProcessPoolExecutor, as_completed

# Filter the CSV entries to look for specific key strings
def filter_csv(input_csv, key_string):
    filtered_rows = []
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if key_string in row['your_column_name_here']:
                filtered_rows.append(row)
    return filtered_rows

# Generate a folder list based on the main folder
def generate_folder_list(main_folder, key_string):
    folder_list = {}
    for root, dirs, files in os.walk(main_folder,max_depth=1):
        for dir in dirs:
            if key_string in dir:
                folder_list[dir] = os.path.join(root, dir)
    return folder_list

# Find .docx files in the specific folder
def find_docx_files(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.docx')]

# Finds the newest Word file based on creation time
def sort_word_files(docx_files):
    return max(docx_files, key=os.path.getctime)

# Extracts values from a Word file based on the regex pattern
def extract_values_from_word(word_file_path, regex_pattern):
    doc = Document(word_file_path)
    values = []
    for para in doc.paragraphs:
        matches = re.findall(regex_pattern, para.text)
        if matches:
            values.extend(matches)
    return values

# Prepare a scraped row object
def initialize_scraped_row(row):
    return {
        'your_key_here': row['your_key_here'],
        'error_message': '',
        'your_value_here': row.get('your_value_here', '')
    }

# Write a row to the output CSV
def write_to_csv(scraped_row, writer):
    print(f"Writing to CSV for {scraped_row['your_key_here']}")
    writer.writerow(scraped_row)

# Main logic for scraping and saving data
def scrape_and_save(input_csv, scraped_csv, key_string, main_folder):
    filtered_rows = filter_csv(input_csv, key_string)
    folder_list = generate_folder_list(main_folder, key_string)
    
    with open(scraped_csv, 'a', newline='', encoding='utf-8') as outfile:
        fieldnames = ['your_key_here', 'your_value_here', 'error_message']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        if not os.path.exists(scraped_csv):
            writer.writeheader()

        for row in filtered_rows:
            scraped_row = initialize_scraped_row(row)
            specific_folder_path = folder_list.get(row['your_key_here'], None)
            
            if specific_folder_path:
                docx_files = find_docx_files(specific_folder_path)
                if docx_files:
                    newest_file = sort_word_files(docx_files)
                    
                    # Annotated Regex Pattern: Modify this pattern as needed
                    regex_pattern = r'your_regex_here'
                    
                    extracted_values = extract_values_from_word(newest_file, regex_pattern)
                    if extracted_values:
                        scraped_row['your_value_here'] = ', '.join(extracted_values)
            
            write_to_csv(scraped_row, writer)

if __name__ == '__main__':
    input_csv = input("Enter the path of the input CSV: ")
    scraped_csv = input("Enter the path of the output CSV: ")
    key_string = input("Enter the key string to look for: ")
    main_folder = input("Enter the main folder path: ")
    
    scrape_and_save(input_csv, scraped_csv, key_string, main_folder)