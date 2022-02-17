#!/usr/bin/env python
#-*- coding: utf-8 -*-


# Types and useful classes Defined by Daseon

import math as m
import random as rd
import copy


def clip(scri, min, max):
    val = scri
    if scri < min:
        val = min
    elif scri > max:
        val = max
    return val

class Vector3:

    def __init__(self,x,y,z=0,LLSS=0,DDSS=(0,0)):
        self.x = x
        self.y = y
        self.z = z
        self.LLSS = LLSS   
        self.DDSS = (DDSS[0]-1, DDSS[1]-1)
    
    def cast(lllist):
        if len(lllist)==2:
            lllist = lllist + [0]
        return Vector3(lllist[0], lllist[1], lllist[2])

    def __repr__(self):
        return 'Vec3'+str(self.vec)

    def __add__(self, other):
        A = self.vec
        B = other.vec
        if len(A) != len(B):
            print("Error : Vector size"+str(len(A)+" and "+str(len(B)) + "missmatch" ))
            return None
        return Vector3(A[0]+B[0], A[1]+B[1], A[2]+B[2])

    def __sub__(self, other):
        A = self.vec
        B = other.vec
        if len(A) != len(B):
            print("Error : Vector size"+str(len(A)+" and "+str(len(B)) + "missmatch" ))
            return None
        return Vector3(A[0]-B[0], A[1]-B[1], A[2]-B[2])

    def __mul__(self, other):
        A = self.vec
        if type(other) is int:
            B = other
            val = Vector3(A[0]*B, A[1]*B, A[2]*B)
        elif type(other) is float:
            B = other
            val = Vector3(A[0]*B, A[1]*B, A[2]*B)
        else:
            B = other.vec
            val = Vector3(A[0]*B[0], A[1]*B[1], A[2]*B[2])
        return val
        
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    @property
    def vec(self):
        return [self.x, self.y, self.z]

    @property
    def vec2D(self):
        return [self.x, self.y]

    def pygameVec(self, DDSS, LLSS):
        return [ self.x*LLSS/2+DDSS[0]/2, -self.y*LLSS/2+DDSS[1]/2 ]


class Integrator:
    def __init__(self, IC, dt):
        self.IC             = IC
        self.dt             = dt
        self.prev           = IC
        self.previnput      = 0
        if type(IC) is Vector3:
            self.previnput  = Vector3(0.,0.,0.)
        self.Result         = IC
    
    def __repr__(self):
        return str(self.Result)

    def step(self, nowval):
        self.Result         = self.prev + ( (nowval)*self.dt + (nowval + self.previnput)*0.5*self.dt )*0.5
        self.prev           = self.Result
        self.previnput      = nowval
        return self.Result

    def reset(self, IC):
        self.prev           = IC
        self.Result         = IC

class Differntiator:
    def __init__(self, dt):
        self.dt             = dt
        self.previnput      = 0
        self.Result         = 0
        self.sofarNorun     = True
    
    def __repr__(self):
        return str(self.Result)

    def step(self, nowval):
        if self.sofarNorun == True:
            self.sofarNorun = False
            self.Result = 0
            self.previnput      = nowval
        else:
            self.Result         = (nowval - self.previnput)/self.dt
            self.previnput      = nowval
        return self.Result

    def reset(self):
        self.previnput           = 0
        self.Result         = 0
        self.sofarNorun     = True

class FirstOrder:
    def __init__(self, num, tau, K, dt):
        self.xinteg         = Integrator(0, dt)
        self.yinteg         = Integrator(0, dt)
        self.prevy          = 0
        self.num, self.tau  = num, tau
        self.K              = K
        self.dt             = dt
    
    def step(self, cmd):
        y = ( self.num*self.xinteg.step(cmd) - self.K*self.yinteg.step(self.prevy) )/self.tau
        self.prevy = y
        return y

    def reset(self):
        self.xinteg         = Integrator(0, self.dt)
        self.yinteg         = Integrator(0, self.dt)
        self.prevy          = 0

class SecondOrder:
    def __init__(self, omega, zeta, dt):
        self.x2integ_1      = Integrator(0, dt)
        self.x2integ_2      = Integrator(0, dt)
        self.yinteg         = Integrator(0, dt)
        self.y2integ_1      = Integrator(0, dt)
        self.y2integ_2      = Integrator(0, dt)
        self.prevy          = 0
        self.omega          = omega
        self.zeta           = zeta
        self.dt             = dt
    
    def step(self, cmd):
        y = self.omega**2 * self.x2integ_2.step(self.x2integ_1.step(cmd))\
            - 2*self.zeta*self.omega * self.yinteg.step(self.prevy)\
            - self.omega**2 * self.y2integ_2.step(self.y2integ_1.step(self.prevy))
        self.prevy = y
        return y

    def reset(self):
        self.x2integ_1      = Integrator(0, self.dt)
        self.x2integ_2      = Integrator(0, self.dt)
        self.yinteg         = Integrator(0, self.dt)
        self.y2integ_1      = Integrator(0, self.dt)
        self.y2integ_2      = Integrator(0, self.dt)
        self.prevy          = 0
