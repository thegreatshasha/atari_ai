from numpy import ndarray
import numpy as np
from collections import deque
import timeit

class RingBuffer():

    def __init__(self, size):
        self.size = size
        self.top = 0
        self.bottom = 0
        #self.data = [0] * self.size
        self.data = np.zeros(self.size, dtype='f')
        self.length = 0

    #@profile
    def append(self, element):
        """ Overwrites the oldest element with """
        self.data[self.top] = element

        """ Increment the size """
        self.length = min(self.length + 1, self.size)
        
        """ Update the top n bottom indexes """
        self.top = (self.top + 1) % self.size
        if self.top == self.bottom:
            self.bottom = (self.top + 1) % (self.size - 1)

        #print (self.data, self.bottom, self.top, self.length)

    #@profile
    def pop(self):
        """ Decrement the size """
        if self.length:
            self.length = min(self.length - 1, self.size)
        else:
            raise AssertionError("Nothing to pop!")

        """ Returns the topmost element """
        top = self.data[self.top-1]
        
        """ Reduce the top index """
        self.top = (self.top -1) % self.size

        #print (self.data, self.bottom, self.top, self.length)
        return top

# rb = RingBuffer(5)
# rb.push(1)
# rb.push(2)
# rb.push(3)
# rb.push(4)
# rb.push(5)
# import pdb; pdb.set_trace()

# """ Some tests """
# rb.push(6)
# rb.push(7)
# rb.push(8)

# rb.pop()
# rb.pop()
# rb.pop()
# rb.pop()
# rb.pop()
#@profile
def buffer_test(buffer, size):
    #size = 10
    """ Some performance tests. Compared with python queue """
    #buffer = deque(maxlen=size)
    
    """ do 1000 pushes and 1000 pops """
    for i in xrange(size):
        buffer.append(i)

    for i in xrange(size):
        buffer.pop()

def ring_buffer_test():
    size = 100000
    rb = RingBuffer(size)
    buffer_test(rb, size)

def dequeue_test():
    size = 100000
    """ Some performance tests. Compared with python queue """
    buffer = deque(maxlen=size)

    zeta = np.array(buffer)

    buffer_test(buffer, size)

#timeit ringbuff_deque_test()
#import pdb; pdb.set_trace()
print "Ring buffer: %f" % timeit.timeit(ring_buffer_test, number=100)
print "Dequeue: %f" % timeit.timeit(dequeue_test, number=100)