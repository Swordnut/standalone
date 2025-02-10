import os
import pandas as pd

def get_csv_files(input_location):
    return [file for file in os.listdir(input_location) if file.endswith('.csv')]

def read_csv_as_utf8(input_location, file):
    # reads a CSV file and ensures it is loaded in UTF-8 encoding
    input_path = os.path.join(input_location, file)
    try:
        # Attempt to read the file with UTF-8 encoding
        dataframe = pd.read_csv(input_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Fallback to ISO-8859-1 if UTF-8 fails
        dataframe = pd.read_csv(input_path, encoding='ISO-8859-1')
    return dataframe

def clean_tbl_name(filename):
    # Cleans table name by removing special characters and converting to lowercase.
    clean_name = (filename.lower().replace(" ","")
                  .replace(",","").replace("$","")
                  .replace("£","").replace("%","")
                  .replace("#","").replace("-","")
                  .replace("@","").replace("~","")
                  .replace("&","").replace('"',"")
                  .replace("'", ""))
    return clean_name.split(".")[0]

def clean_col_name(dataframe):
    # Cleans column names and ensures values in string columns are formatted properl
    dataframe.columns = [x.lower().replace(" ","_").replace(",","_")
                         .replace("$","").replace("£","").replace("%","")
                         .replace("#","").replace("-","_").replace("@","_")
                         .replace("~","_").replace("&","_").replace("\n","_") for x in dataframe.columns]
    for col in dataframe.columns:
        if dataframe[col].dtype == 'object':  # Only apply to string columns
            dataframe[col] = dataframe[col].str.replace("\n", "").str.replace("'", "").str.replace('"',"")
            
    return dataframe

    

def save_cleaned_csv(output_location, filename, dataframe):
    # Saves the cleaned DataFrame as a CSV in UTF-8 format
    output_path = os.path.join(output_location, clean_tbl_name(filename) + '.csv')
    dataframe.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Saved cleaned CSV to {output_path}")

def main():
    input_location = input('Enter CSV directory path: ')
    output_location = os.path.join(input_location, 'result')
    
    # Create cleaned directory if it doesn't exist
    if not os.path.exists(output_location):
        os.makedirs(output_location)

    
    csv_files = get_csv_files(input_location)
    
    
    for file in csv_files:
        # Read the CSV file with proper encoding
        dataframe = read_csv_as_utf8(input_location, file)
        # Clean column names and string data
        dataframe = clean_col_name(dataframe)
        # Save the cleaned file to the output folder
        save_cleaned_csv(output_location, file, dataframe)

if __name__ == "__main__":
    main()
