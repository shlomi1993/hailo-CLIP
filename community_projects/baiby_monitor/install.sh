#!/bin/bash

sudo apt update

pip3 install -r requirements.txt

mkdir -p resources
curl -L "https://drive.usercontent.google.com/uc?id=1Myk5VzIQWYDbjp-zYiFjUwQn15HQyuPU&export=download" -o "resources/brahms-lullaby.mp3"

echo "Installation of B-AI-by-Monitor was completed."
