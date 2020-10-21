#!/bin/sh

if [ "$#" -lt 1 ]; then
    echo "Error : missing avatar name in the command line as a unique argument."
    exit 0
fi

if [ "$1" == "--help" ]; then
    echo "You must enter exactly your avatar name in the command line as a unique argument."
    echo "EXAMPLE : ./zip-and-upload.sh xenon"
    exit 0
fi

# Check if Zeppelin notebooks are available
if [ -d "/mnt/var/lib/zeppelin/notebook" ]; then
    cp -r /mnt/var/lib/zeppelin/notebook .
else 
    echo "Warnig: Zeppelin notebooks directory does not exist."
fi

# Create the archive and upload it to the bucket
zip -r work-dir.zip * -x "*.sh"
bucketname="${1,,}-eur"
aws s3 cp work-dir.zip s3://"$bucketname"

# Remove temporary files
rm -rf notebook/ work-dir.zip
