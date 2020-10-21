#!/bin/sh
AVATAR[0]="KRYPTON"
AVATAR[1]="XENON"
AVATAR[2]="ARGON"
AVATAR[3]="BORON"
AVATAR[4]="COBALT"
AVATAR[5]="CESIUM"
AVATAR[6]="CHROMIUM"
AVATAR[7]="PLATINUM"
AVATAR[8]="BARIUM"
AVATAR[9]="OSMIUM"

for i in "${AVATAR[@]}"
do
	bucketname="${i,,}-eur"
	aws s3api create-bucket --bucket ${bucketname} --create-bucket-configuration LocationConstraint=eu-west-3
	# echo "${bucketname}"
done
