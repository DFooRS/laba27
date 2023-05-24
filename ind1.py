#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread, Condition
from queue import Queue
import time


G = 6.6743e-11 #Гравитационная постоянная
MASS_EARTH = 5.97e24 #Масса земли
RADIUS_EARTH = 6.37e6 #Радиус земли

q_pos = Queue()
q_vel = Queue()
q_time = Queue()
cv = Condition()


def satellite_motion():
    """
    Функция для вычисления координат и скоростей спутника.
    """
    x0 = RADIUS_EARTH + 500e3
    v0 = ((G * MASS_EARTH) / x0) ** 0.5
    dt = 1
    t = 0
    x, y, z = x0, 0, 0
    vx, vy, vz = 0, v0, 0

    while t < 10:
        with cv:
            t += dt
            r = (x ** 2 + y ** 2 + z ** 2) ** 0.5
            Fg = -G * MASS_EARTH / r ** 2

            ax = Fg * x / r
            ay = Fg * y / r
            az = Fg * z / r

            vx += ax * dt
            vy += ay * dt
            vz += az * dt

            x += vx * dt
            y += vy * dt
            z += vz * dt

            q_pos.put((x, y, z))
            q_vel.put((vx, vy, vz))
            q_time.put(t)

            cv.notify()
            time.sleep(0.5)

def print_motion():
    """
    Функция для вывода текущих координат и скоростей спутника
    """
    while True:
        with cv:
            while q_pos.empty() or q_vel.empty() or q_time.empty():
                cv.wait()
            try:
                x, y, z = q_pos.get_nowait()
                vx, vy, vz = q_vel.get_nowait()
                t = q_time.get_nowait()
                print(f"Координаты({t}): ({x}, {y}, {z})")
                print(f"Скорости({t}): ({vx}, {vy}, {vz})")
            except:
                pass
            time.sleep(0.5)


if __name__ == '__main__':
    th_motion = Thread(target=satellite_motion)
    th_print = Thread(target=print_motion)
    th_motion.start()
    th_print.start()
