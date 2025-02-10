import csv
import re

# note - change this to a json import? 
grid_square_offsets = {
  "SV": [0, 0],
  "SW": [100000, 0],
  "SX": [200000, 0],
  "SY": [300000, 0],
  "SZ": [400000, 0],
  "TV": [500000, 0],
  "TW": [600000, 0],
  "SQ": [0, 100000],
  "SR": [100000, 100000],
  "SS": [200000, 100000],
  "ST": [300000, 100000],
  "SU": [400000, 100000],
  "TQ": [500000, 100000],
  "TR": [600000, 100000],
  "SL": [0, 200000],
  "SM": [100000, 200000],
  "SN": [200000, 200000],
  "SO": [300000, 200000],
  "SP": [400000, 200000],
  "TL": [500000, 200000],
  "TM": [600000, 200000],
  "SF": [0, 300000],
  "SG": [100000, 300000],
  "SH": [200000, 300000],
  "SJ": [300000, 300000],
  "SK": [400000, 300000],
  "TF": [500000, 300000],
  "TG": [600000, 300000],
  "SA": [0, 400000],
  "SB": [100000, 400000],
  "SC": [200000, 400000],
  "SD": [300000, 400000],
  "SE": [400000, 400000],
  "TA": [500000, 400000],
  "TB": [600000, 400000],
  "NV": [0, 500000],
  "NW": [100000, 500000],
  "NX": [200000, 500000],
  "NY": [300000, 500000],
  "NZ": [400000, 500000],
  "OV": [500000, 500000],
  "OW": [600000, 500000],
  "NQ": [0, 600000],
  "NR": [100000, 600000],
  "NS": [200000, 600000],
  "NT": [300000, 600000],
  "NU": [400000, 600000],
  "OQ": [500000, 600000],
  "OR": [600000, 600000],
  "NL": [0, 700000],
  "NM": [100000, 700000],
  "NN": [200000, 700000],
  "NO": [300000, 700000],
  "NP": [400000, 700000],
  "OL": [500000, 700000],
  "OM": [600000, 700000],
  "NF": [0, 800000],
  "NG": [100000, 800000],
  "NH": [200000, 800000],
  "NJ": [300000, 800000],
  "NK": [400000, 800000],
  "OF": [500000, 800000],
  "OG": [600000, 800000],
  "NA": [0, 900000],
  "NB": [100000, 900000],
  "NC": [200000, 900000],
  "ND": [300000, 900000],
  "NE": [400000, 900000],
  "OA": [500000, 900000],
  "OB": [600000, 900000],
  "HV": [0, 1000000],
  "HW": [100000, 1000000],
  "HX": [200000, 1000000],
  "HY": [300000, 1000000],
  "HZ": [400000, 1000000],
  "JV": [500000, 1000000],
  "JW": [600000, 1000000],
  "HQ": [0, 1100000],
  "HR": [100000, 1100000],
  "HS": [200000, 1100000],
  "HT": [300000, 1100000],
  "HU": [400000, 1100000],
  "JQ": [500000, 1100000],
  "JR": [600000, 1100000],
  "HL": [0, 1200000],
  "HM": [100000, 1200000],
  "HN": [200000, 1200000],
  "HO": [300000, 1200000],
  "HP": [400000, 1200000],
  "JL": [500000, 1200000],
  "JM": [600000, 1200000]
}

prefixes = [
    [ 'SV', 'SW', 'SX', 'SY', 'SZ', 'TV', 'TW' ],
    [ 'SQ', 'SR', 'SS', 'ST', 'SU', 'TQ', 'TR' ],
    [ 'SL', 'SM', 'SN', 'SO', 'SP', 'TL', 'TM' ],
    [ 'SF', 'SG', 'SH', 'SJ', 'SK', 'TF', 'TG' ],
    [ 'SA', 'SB', 'SC', 'SD', 'SE', 'TA', 'TB' ],
    [ 'NV', 'NW', 'NX', 'NY', 'NZ', 'OV', 'OW' ],
    [ 'NQ', 'NR', 'NS', 'NT', 'NU', 'OQ', 'OR' ],
    [ 'NL', 'NM', 'NN', 'NO', 'NP', 'OL', 'OM' ],
    [ 'NF', 'NG', 'NH', 'NJ', 'NK', 'OF', 'OG' ],
    [ 'NA', 'NB', 'NC', 'ND', 'NE', 'OA', 'OB' ],
    [ 'HV', 'HW', 'HX', 'HY', 'HZ', 'JV', 'JW' ],
    [ 'HQ', 'HR', 'HS', 'HT', 'HU', 'JQ', 'JR' ],
    [ 'HL', 'HM', 'HN', 'HO', 'HP', 'JL', 'JM' ]
]

# Convert NGR to easting and northing
def ngr_to_east_north(grid_ref):
    match = re.match(r'^([A-Z]{2})(\d+)$', grid_ref.upper().replace(" ", ""))  
    if not match:
        return None, None
    prefix, digits = match.groups()
    if prefix not in prefixes:
        print("prifix does not match known grid squares")
        return None, None
    

    offset_x, offset_y = grid_square_offsets[prefix]
    length = len(digits) // 2
    scale = 10 ** (5 - length)
    easting = offset_x + int(digits[:length]) * scale
    northing = offset_y + int(digits[length:]) * scale
    return easting, northing

# Process the CSV file
def process_csv(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['easting', 'northing']
        rows = []

        for row in reader:
            for column in row:
                if "NGR" in column.upper():  # Identify the NGR column
                    ngr_column = column
                    break
            else:
                raise ValueError("No NGR column found in the CSV file.")

            ngr = row[ngr_column]
            easting, northing = ngr_to_east_north(ngr)
            row['Easting'] = easting
            row['Northing'] = northing
            rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


input_csv = 'input.csv'
output_csv = 'output.csv'
process_csv(input_csv, output_csv)
