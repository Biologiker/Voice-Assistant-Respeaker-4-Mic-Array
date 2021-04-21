@echo off
echo downloading pixel ring...

cd ..
git clone --depth 1 https://github.com/respeaker/pixel_ring.git
cd pixel_ring

echo installing pixel ring...
pip install -U -e .

echo installing pip requirement...
cd ..
pip install -r requirements.txt

echo done!