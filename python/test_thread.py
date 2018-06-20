#coding=utf-8
from multiprocessing import Pool
from threading import Thread

from multiprocessing import Process


def loop():
    while True:
        pass

if __name__ == '__main__':

    for i in range(3):
        t = Thread(target=loop)
        t.start()

    while True:
        pass

