#!/bin/bash

echo "==>dependencies setup for deep_q_rl"

echo "==>updating current package..."
sudo apt-get update

echo "==>installing OpenCV..."
sudo apt-get install python-opencv

echo "==>installing Matplotlib..."
sudo apt-get install python-matplotlib python-tk

echo "==>installing Theano ..."
# some dependencies ...
sudo apt-get install python-numpy python-scipy python-dev python-pip python-nose g++ libopenblas-dev git
pip install --user --upgrade --no-deps git+git://github.com/Theano/Theano.git

echo "==>installing Keras ..."
pip install keras

# Packages below this point require downloads. 
if [ ! -d "./ALE" ]
then
echo "==>installing ALE ..."

# dependencies ...
sudo apt-get install libsdl1.2-dev libsdl-gfx1.2-dev libsdl-image1.2-dev cmake

git clone https://github.com/mgbellemare/Arcade-Learning-Environment ALE
cd ./ALE
cmake -DUSE_SDL=ON -DUSE_RLGLUE=OFF .
make -j2
pip install --user .
cd ..
fi

echo "==>All done!"