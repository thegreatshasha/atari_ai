import plotly.plotly as p
import datetime
import time
import numpy as np
import json
from plotly.graph_objs import *
import timeit
from multiprocessing import Pool
import threading


def block(obj):
        time.sleep(5)
        print obj

class Plotter:

    def __init__(self):
        self.config = {
            'streaming_token': 'c8rv8cp68b'
        }
        self.plotfile = str(datetime.datetime.now())
        self.plot =  p.iplot([{'x': [], 'y': [], 'type': 'scatter', 'mode': 'lines+markers',
                    'stream': {'token': self.config['streaming_token'], 'maxpoints': 1000000}
                  }],
                filename=self.plotfile, fileopt='overwrite')

        self.url = self.plot.resource
        print self.url
        self.stream = p.Stream(self.config['streaming_token'])
        self.stream.open()

    def write(self, x, y):
        self.stream.write({'x': x, 'y': y})
        #thread = threading.Thread(target=self.stream.write, args=({'x':x, 'y':y},))
        #thread.daemon = True                            # Daemonize thread
        #thread.start()
        #res = self.pool.apply(block, args=(3,))