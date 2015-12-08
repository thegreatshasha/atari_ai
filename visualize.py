import plotly.plotly as p
import datetime
import time
import numpy as np
import json
from plotly.graph_objs import *
import timeit

class Plotter:

    def __init__(self):
        self.config = {
            'username': 'thegreatshasha',
            'api_key': 'vmodg4jjyv',
            'streaming_token': 'xudit15e6d'
        }

        self.plot =  p.iplot([{'x': [], 'y': [], 'type': 'scatter', 'mode': 'lines+markers',
                    'stream': {'token': self.config['streaming_token'], 'maxpoints': 80}
                  }],
                filename='Time-Series', fileopt='overwrite')

        self.url = self.plot.resource
        print self.url
        self.stream = p.Stream(self.config['streaming_token'])
        self.stream.open()

    def write(self, x, y):
        self.stream.write({'x': x, 'y': y})

# plotly = Plotter()

# def tests():
    
#     for i in range(10):
#         #print 10, 10
#         plotly.write(10, 10)

# print timeit.timeit(tests, number=1000)