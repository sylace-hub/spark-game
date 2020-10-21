#!/bin/sh

if [ "$#" -lt 1 ]; then
    echo "Error : missing avatar name in the command line as a unique argument."
    exit 0
fi

if [ "$1" == "--help" ]; then
    echo "You must enter exactly your avatar name in the command line as a unique argument."
    echo "EXAMPLE : ./download-and-unzip.sh xenon"
    exit 0
fi

bucketname="${1,,}-eur"
aws s3 cp s3://"$bucketname"/work-dir.zip .
unzip work-dir.zip && rm work-dir.zip
