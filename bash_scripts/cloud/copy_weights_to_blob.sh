#!/bin/bash
if [ -z "$1" ]
  then
    echo "No file argument supplied, exit"
    exit
fi
echo "File to be transfered:"$1
echo "Start copying..."
current_date=$(date '+%Y%m%d%H%M%S')
file_dir="$(dirname "${1}")"
file_name="$(basename "${1}")"
echo "$current_date"
echo "$file_dir"
temp_file="$file_dir/$current_date-$file_name"
cp $1 $temp_file
azcopy copy $temp_file <sas_token_url>
rm $temp_file
echo "Copy fininised"