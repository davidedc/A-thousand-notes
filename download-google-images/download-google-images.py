# For this you'll need to install https://github.com/RiddlerQ/simple_image_download
# which requires pip, which on OSX on m1 machines means:
#
# 1. Install pip:
#      curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#      python3 get-pip.py 
# 2. Once pip is ready, you can install simple_image_download
#      python3 -m pip install simple_image_download
#
# Them (example):
#      python3 download-google-images.py "red dog" -n 10

from simple_image_download import simple_image_download as simp

import argparse

parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('searchwords')
parser.add_argument('-n', type=int, default=100, help='how many images')
args = parser.parse_args()

response = simp.simple_image_download

response().download(args.searchwords, args.n)
