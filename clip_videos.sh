#!/bin/bash

# Check if the input directory is provided as a command-line argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 input_directory"
    exit 1
fi

input_dir="$1"  # Set the input directory from the command-line argument

# Iterate over all .mp4 and .mkv files in the input directory
for input_file in "$input_dir"/*.mp4 "$input_dir"/*.mkv; do
    # Check if the file is a regular file
    if [ -f "$input_file" ]; then
        # Run the Python script for the current input file
        python3 clip_extractor.py "$input_file"
    fi
done
