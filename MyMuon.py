"""
MyMuonX, a class for Muon Lifetime Measurement

Authors: Azid Harun

Date :  05/10/2018

"""

# Import required packages
import numpy as np
from sympy import *

class MyMuonX(object):
    """
    Class for Muon Lifetime Measurement.
    
    Properties:
    low_limit(float)   -  lower limit of interval
    high_limit(float)  -  higher limit of interval
    mean(float)        -  muon decay rate ( 1 / muon lifetime)
    num(integer)       -  number of muon
    
    Methods:
    * random_x         -  muon decay rate generator
    * f                -  probability density function(pdf) evaluator
    * integralNumeric  -  1. average value of a function, <f> calculator
                          2. area under the curve calculator
    """

    def __init__(self, low_limit, high_limit, mean, num = 1000):
        """
                Initialise a MyMuonX instance
        
                :param low_limit: lower limit of interval as float
                :param high_limit: higher limit of interval as float
                :param mean: muon decay rate as float
                :param num: number of muon as integer
        """

        self.mean = mean
        self.num = num
        self.low = low_limit
        self.high = high_limit

    def __iter__(self):
        """    Returns the iterator object and implicitly called at the start of loops    """
        
        self.n = 1
        return self

    def __next__(self):
        """    Simulate a decay rate for every muons    """
        
        if self.n > self.num:
            raise StopIteration
        else:
            self.n += 1
            return self.random_x()

    def f(self, x):
        """    Return the pdf point at the given x    """

        return self.mean*exp(-x*self.mean)

    def random_x(self):
        """
                Return - x1, the random decay rate within the interval, 
                       - y1, its pdf point
                       
                         as tuple tuple.
                         
				y2, random point between origin and its pdf point
				
                If y2 is not less than y1, the function is repeated until the condition is true.
        """

        fmax = self.mean
        x1 = np.random.uniform(self.low, self.high)
        y1 = self.f(x1)
        y2 = fmax*np.random.uniform()
        while y2 > y1:
            x1 = np.random.uniform(self.low, self.high)
            y1 = self.f(x1)
            y2 = fmax*np.random.uniform()
        return (x1, y1)
        # if y2 < y1:
        #     return (x1, y1)
        # else:
        #     return self.random_x()

    def integralNumeric(self, data_list, area=True):
        """
                If area is true, return area under the curve.
                Otherwise, return average value of a function, <f>        
        """

        f_ave = sum(data_list)/len(data_list)
        if area:
            area = (self.high-self.low)*f_ave
            return area
        else:
            return f_ave

