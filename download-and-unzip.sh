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

# Download data archive for the s3 bucket
bucketname="${1,,}-eur"
aws s3 cp s3://"$bucketname"/work-dir.zip .
unzip work-dir.zip

if [ -d "./notebook" ]; then
    if [ ! -d "/mnt/var/lib/zeppelin/notebook" ]; then
	echo "Info : Zeppelin notebooks does not exist, create it."
        sudo mkdir -p /mnt/var/lib/zeppelin/notebook
    fi
    sudo cp -r ./notebook/* /mnt/var/lib/zeppelin/notebook
    # TODO : y a surement un chown pour les notebooks copiés mais je sais pas a qui ? 
fi

# Remove temporary files
rm -rf work-dir.zip ./notebook
