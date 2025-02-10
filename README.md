# standalone
python scripts for various processing tasks

## CSV_Cleaner_batch_user_input

This script identifies all .csv fiiles in a folder (user input filepath) and converts them to utf8. It then cleans up the file name and headers to remove unhelpful characters like special characters and spaces, either delting the character or replacing with an underscore
Output is saved in a new subfolder

## csv_concatenator

Simple script to concatenate all csv files in a user input folder. Appends all rows without replicating headers

## scrape_files_in_folders_for_strings

This may need a little tweaking to streamline entering variables

This script looks at single column in a user input csv for a reference string (just values, not patterns). It uses that reference string to identify folders and files that are relevant to your task. It will search files (currently limited to .docx) and can sort or ignore based on preference (currently set to only look at the newest file). 
It will search through documents to try to find strings that match pattern you have specified with regex and return the results into a cvs output. 
Use it to find things like who is noted a "author" or, what the postcode of the project was, or to extract the summary page etc. I use it to find values for things that people "should" enter into whatever doc management system, but always fail to. 

