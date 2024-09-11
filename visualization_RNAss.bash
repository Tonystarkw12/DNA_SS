#!/bin/bash
#This script is for batch generating images of RNA secondary structures
#Usage: bash visualization_RNAss.bash <input folder> <output folder> 
# First, there are two situations, one is the ct file and the other is the dbn file.


# This script is for batch generating images of RNA secondary structures
# Usage: bash visualization_RNAss.bash <input folder> <output folder>


# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: bash $0 <input folder> <output folder>"
    exit 1
fi

input_folder="$1"
output_folder="$2"
mkdir -p "$output_folder"
# Check if the input folder exists
if [ ! -d "$input_folder" ]; then
    echo "Input directory '$input_folder' does not exist or is not a directory."
    exit 1
fi

# Create the output folder if it does not exist
if [ ! -d "$output_folder" ]; then
    echo "Output directory '$output_folder' does not exist or is not a directory."
fi

# Process each file in the input folder
for file in "$input_folder"/*; do
    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"
        if ! java -cp VARNAv3-93.jar fr.orsay.lri.varna.applications.VARNAcmd -i "$file" -o "$output_folder/$filename.svg"; then
            echo "Visualization failed for $file"
            continue
        fi
done

