#!/bin/bash

declare -a arr=("17edc406eee4d26a0b2b36ac98f1acb078495e74"
                "038c4cebfb6b44131e9f5c47dec578d8f779bb20"
                "5fa74ba8d88d62d5abe0462d7ffc905fca23ed61"
                "9b7e81d49c5ca7d5ca7a13e160d508c58466525b"
                "9cddf22cbc9f9b187d8029dd98068aaee0a2786e"
                "cab3485905d4e0a41b0c2a332689addff2b4d814"
                "d339dbf534905f10a0b834d5ec421b4843e5cfc7"
                "62c9c8141b7ef617aa06ba6aa870cc6b90036579"
                "290e6cb89e01062b7153e3a4954025fe5e36ae12"
                "c0c3625860fb598e5a4d33639e5be1f36977058f"
                "b06fb9b451bb60960ccbe12fccc5a9c412c5e5b5"
                "e15a8c681a960b2173b97de48947143e382ab8f8"
                "8eda6877a45a62e4f8f1f5c0a1f4bd53e024fa9d"
                "4159c21784676710e406f4930d9218fdd341ebd7"
                "9f7acc8bd49b4231ee69c50122359e9501f7332a"
                "982f3e06ba429d39d8b8c1168b6c43312f847504"
                "c2d53b39c7830a3604c1b03219df5f83ddf0e528"
                "1ef99423526f32c7b787e8cbc0755c3df15640b2"
                "44c880c810a88f57db6882fe725685078825f4f2"
                "73af5823d1db47c42787840ee79e44502eb69fba"
                "14625e60f62b582e60f53172182b766212b25acc"
                "aeb4780a28f80af566747d87d59975f55670217a"
                "451595f32ea83553a1414dda222cd4dc8e79e018"
                "93da74adb49ef39f2ecc8c0b2244569a32f5d122"
                "a1de332a25512a50569e4ceed0e9a7a5f628ac3c"
                )
i=1
for hash in "${arr[@]}"
do
    echo "============>$i/${#arr[@]}<=========="
    git checkout "$hash" > /dev/null
    sonar-scanner
    ((i++))
done
git checkout master