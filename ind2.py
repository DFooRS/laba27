#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread, Condition
from math import log, sqrt
from queue import Queue


EPS = .0000001

q = Queue()
cv = Condition()

def sum_func(x):
    with cv:
        summ = x
        prev = 0
        i = 1
        while abs(summ - prev) > EPS:
            prev = summ
            summ += x ** (i * 2 + 1) / (i * 2 + 1)
            i += 1
        q.put(summ)
        cv.notify()


def check_func(x):
    with cv:
        while q.empty():
            cv.wait()
        checking = q.get()
        res = log(sqrt((1 + x) / (1 - x)))
        print(f"Sum is: {checking}")
        print(f"Check: {res}")


if __name__ == '__main__':
    x = 0.35
    th1 = Thread(target=sum_func, args=(x,))
    th2 = Thread(target=check_func, args=(x,))
    th1.start()
    th2.start()
