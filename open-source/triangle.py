#!/usr/bin/python3

import math
class triangle():
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c

    def draw(self):
        self.C=math.acos((self.a**2 + self.b**2 - self.c**2)/(2 * self.a * self.b)) * 180 /math.pi
        self.B=math.acos((self.a**2 + self.c**2 - self.b**2)/(2 * self.a * self.c)) * 180 /math.pi
        self.A=math.acos((self.c**2 + self.b**2 - self.a**2)/(2 * self.c * self.b)) * 180 /math.pi

