import os
import rawpy
import imageio

def convert_cr2_files_in_directory(input_directory):

    for root, dirs, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.CR2') or filename.endswith('.cr2'):
                cr2_file_path = os.path.join(root, filename)
                output_folder = os.path.join(root, 'converted')
                os.makedirs(output_folder, exist_ok=True)
                output_jpg_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpg')
                convert_cr2_to_jpg(cr2_file_path, output_jpg_path)
                print("Converted:", cr2_file_path)  # Print progress indicator

def convert_cr2_to_jpg(cr2_file_path, output_jpg_path):

    with rawpy.imread(cr2_file_path) as raw:
        rgb = raw.postprocess()
        imageio.imsave(output_jpg_path, rgb)

# Example usage:
input_directory = input("Enter the path to the directory containing CR2 files: ")
convert_cr2_files_in_directory(input_directory)