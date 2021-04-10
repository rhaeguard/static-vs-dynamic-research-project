#!/bin/bash

# basically copy this file
# and commits-and-dates file to the repo folder
# and run it

arr=( $(cat commits-and-dates | awk '{print $1}') )

i=1
for hash in "${arr[@]}"
do
    echo "============>$i/${#arr[@]}<=========="
    git checkout "$hash" > /dev/null
    sonar-scanner
    ((i++))
done
git checkout master