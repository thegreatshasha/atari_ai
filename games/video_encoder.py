#!/usr/bin/python

import subprocess
import numpy as np

def getIfromRGB(rgb):
    rgb = rgb.astype('int32')
    red = rgb[:,:,0]
    green = rgb[:,:,1]
    blue = rgb[:,:,2]
    print red, green, blue
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

class VideoSink(object) :
  def __init__( self, size, filename="output", rate=1, byteorder="bgra" ) :
    self.size = size
    cmdstring  = ('mencoder',
      '/dev/stdin',
      '-demuxer', 'rawvideo',
      '-rawvideo', 'w=%i:h=%i'%size[::-1]+":fps=%i:format=%s"%(rate,byteorder),
      '-o', filename+'.avi',
      '-ovc', 'lavc',
      )
    self.p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE, shell=False)

  def run(self, image) :
    assert image.shape == self.size
#   image.swapaxes(0,1).tofile(self.p.stdin) # should be faster but it is indeed slower
    self.p.stdin.write(image.tostring())
  def close(self) :
    self.p.stdin.close()

  
if __name__ == "__main__" :
  import sys
  data = np.load('frames.npy')
  from PIL import Image
  data = data[2:len(data)]
  W, H = data.shape[1], data.shape[2]
  video = VideoSink((H,W), "model_random", rate=8, byteorder="bgra")
  for rgb in data:
    img = getIfromRGB(rgb)
    video.run(img)
  video.close()