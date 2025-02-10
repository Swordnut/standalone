# standalone
python scripts for various processing tasks

## batch__cr2_to_jpg

simple script to find all .cr2 files in a user input folder and convert them to .jpg. 
Output is saved in a new sub-folder

## CSV_Cleaner_batch_user_input

This script identifies all .csv fiiles in a folder (user input filepath) and converts them to utf8. It then cleans up the file name and headers to remove unhelpful characters like special characters and spaces, either delting the character or replacing with an underscore
Output is saved in a new subfolder

## csv_concatenator

Simple script to concatenate all csv files in a user input folder. Appends all rows without replicating headers

## georaster_catalogue_with_bboxes

This script finds all georefferenced files in a folder (and optionaly, its subfolders). It generates a bounding box and saves attributes for the filepath, crs, coordinates and saves the reult as a .gpkg

This still may need some tweaking to get the UI more useful. Currently I need ot add a user input field for skip_keywords list values
It does cause issues with memory when accessing cloud document archives, but I think that is mostly to do with the cloud archive than the script.
The script is threaded to speed things up. That means it saves in batches but I have not implemented a method to concatenate the output. 

Edit the script to input a list of folder name elemnts to skip past
Select a folder
select whether to include sub-folders
select your default crs for output 
Let it run and monitor the output message box. It should tell you where its looking and what its finding.  

## NGR_to_E_N

Work in Progress

Converts a column of NGR cordinates (british national grid coords formatted as a string e.g., TQ12341234) to integer eastings and northings (x/y coordsinates in British National Grid Projection)
Im not sure how it would handle the grids at the extreme south-west

## scrape_files_in_folders_for_strings

This may need a little tweaking to streamline entering variables

This script looks at single column in a user input csv for a reference string (just values, not patterns). It uses that reference string to identify folders and files that are relevant to your task. It will search files (currently limited to .docx) and can sort or ignore based on preference (currently set to only look at the newest file). 
It will search through documents to try to find strings that match pattern you have specified with regex and return the results into a cvs output. 
Use it to find things like who is noted a "author" or, what the postcode of the project was, or to extract the summary page etc. I use it to find values for things that people "should" enter into whatever doc management system, but always fail to. 

