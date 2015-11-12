#!/bin/sh

for file in css/*
do
    echo $file
    sed -i 's/googleapi/useso/g' $file
done
