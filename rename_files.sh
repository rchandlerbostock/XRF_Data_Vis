#!/bin/bash

# Define the part of the string to remove 
# This is the plate name that Dundee add onto the file name
STRING_TO_REMOVE="_CoV_Ladder_STNV-C4_"

# Loop through files in the current directory
for FILE in *"$STRING_TO_REMOVE"*; do
    # Check if the file exists to avoid errors
    if [ -e "$FILE" ]; then
        # Remove the defined string and the next three characters
        NEW_FILE="${FILE//$STRING_TO_REMOVE/}"
        # Remove the last seven characters 
        #these are the last three real characters and the .fsa extension
        NEW_FILE="${NEW_FILE:0:${#NEW_FILE}-7}"  
        # Add the .fsa extension back in
        NEW_FILE="$NEW_FILE.fsa"
        # Rename the file
        mv "$FILE" "$NEW_FILE"
        echo "Renamed: $FILE to $NEW_FILE"
    fi
done
# In terminal remember to make the script executable with chmod +x rename_files.sh
# Then run the script with ./rename_files.sh
# Script should be in the same folder as the files you want to rename
