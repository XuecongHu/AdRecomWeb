# -*- coding:utf-8 -*-
__author__ = 'frank'
from numpy import *
import numpy as np


def cos_sim(array_a, array_b):
    return dot(array_a, array_b) / (np.linalg.norm(array_a) * np.linalg.norm(array_b))

if __name__ == '__main__':

    data = [1,2,3,66,442,7,442]

    result = [0, 0]

    for i in range(len(data)):
        index = -1
        gap = -1
        for j in range(len(result)):
            if data[i] - result[j] > gap:
                gap = data[i] - result[j]
                index = j

        if index!=-1:
            result[index] = data[i]

    print result