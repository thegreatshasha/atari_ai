import random
import numpy as np

def cdf(items):
    sum = 0
    cdf = []
    for index, item in enumerate(items):
        sum += items[index]
        cdf.append(sum)
    return cdf

def match(items, index, value):
    if not index:
        return index

    if items[index] < value:
        return 1
    else:
        if items[index-1] < value:
            return 0
        else:
            return -1

def binary_search(items, value, begin, end):
    mid = (begin + end) / 2
    
    res = match(items, mid, value)
    
    if res == -1:
        return binary_search(items, value, begin, mid)

    elif res == 0:
        return mid
    
    else:
        return binary_search(items, value, mid+1, end)

def select_with_probability(items, probs):
    cdf_probs = cdf(probs)
    rand_float = random.random()

    found = binary_search(cdf_probs, rand_float, 0, len(cdf_probs)-1)

    return items[found]

def statistical_tests():
    unique = {1:0.0, 2:0.0, 3:0.0}
    probs = [0.1, 0.7, 0.2]

    for i in range(100000):
        unique[select_with_probability([1,2,3], probs)] += 1

    total = sum(unique.values())
    for key in unique:
        unique[key] = (unique[key] / total)

    arr = unique.values()
    percent_error = (np.mean(np.absolute(np.array(arr) - np.array(probs))) / np.mean(arr))

    assert(percent_error < 0.001)

if __name__ == '__main__':
    statistical_tests()