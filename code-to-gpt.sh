#!/bin/bash

# Define the output file
output_file="project_summary.txt"

# Clear the output file if it exists
> "$output_file"

# Function to minify Python files by removing comments and unnecessary whitespace
minify_python() {
  sed '/^\s*#/d;/^\s*$/d' "$1" | tr -s '[:space:]' ' '
}

# Check if the app directory exists
if [ -d "./app" ]; then
  # Find all .py files in the app directory and subdirectories
  find ./app -type f -name "*.py" | while read file; do
    echo "Processing $file..." >> "$output_file"
    echo "----------------------------------------" >> "$output_file"
    echo "File: $file" >> "$output_file"
    echo "----------------------------------------" >> "$output_file"

    # Minify and append the Python file to the output file
    minify_python "$file" >> "$output_file"

    echo -e "\n\n" >> "$output_file"
  done

  echo "Summary created in $output_file."
else
  echo "The app directory does not exist."
fi
