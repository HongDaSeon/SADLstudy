#!/usr/bin/env python
# coding: utf-8

import pygame as pg
import sys

C_Missile       = (50, 100, 200)
C_NoflyZone     = (100, 100, 100)
C_lidarSens     = (150, 150, 200)
C_Target        = (200, 50, 100)
C_lGrey         = (200, 200, 200)
C_black         = (0,0,0)
C_Font          = (193, 243, 255)

LLSS = 0
DDSS = 0


class VisualizationPygame:
    
    def __init__(self, dispSize, lookScale, Title,joy=False):
        global LLSS, DDSS
        LLSS = lookScale
        DDSS = (dispSize[0]-1, dispSize[1]-1)
        self.LLSS   = LLSS
        self.DDSS   = DDSS
        self.dSize  = dispSize
        self.LS     = lookScale
        self.controller = None
        self.Title      = Title
        self.acc        = 0
        self.pause      = False
        self.resume     = False
        
        pg.init()
        self.GameFont   = pg.font.SysFont('arialblack', 30, True, False)
        self.texTile    = self.GameFont.render("SCORE ", True, C_Font)
        
        if joy:
            pg.joystick.init()
            try:
                self.controller = pg.joystick.Joystick(0)
                self.controller.init()
                print ("Joystick_Paired: {0}".format(self.controller.get_name()))
            except pg.error:
                print ("None of or Invalid joystick connected")
        
        self.Disp = pg.display.set_mode((self.dSize[0], self.dSize[1]))
        pg.display.set_caption(self.Title)
        self.centre = (self.dSize[0]/2, self.dSize[1]/2)

    def draw_circle(self, center, radius):
        pg.draw.circle(self.Disp, C_NoflyZone, self.in2Dcenter(center), radius)

    def draw_poly(self, vertices, color=C_Target, width=2):
        pg.draw.polygon(self.Disp, color, [ self.in2Dcenter(vertices[0]),\
                                            self.in2Dcenter(vertices[1]),\
                                            self.in2Dcenter(vertices[2]),
                                            self.in2Dcenter(vertices[3])], width)

    def draw_img(self, img, scale, pos):
        self.Disp.blit( img, pos )

    def draw_Text(self, text, size, pos):
        self.GameFont   = pg.font.SysFont('arialblack', size, True, False)
        self.texTile    = self.GameFont.render(text, True, C_Font)
        self.Disp.blit( self.texTile, pos)

    def update(self):
        pg.display.update()

    def event_get(self, acc):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print('goodbye')
                sys.exit()
            if event.type == pg.JOYAXISMOTION:  # Joystick
                pass
            if event.type == pg.JOYBUTTONDOWN:  
                print("Joystick Button pressed")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    print("^keyPressed")
                    self.acc = acc
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    print("keyReleased")
                    self.acc = 0
            if not self.pause:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        print("Play")
                        self.pause = True
                if event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        print("Paused")
                        self.pause = False
            if self.pause:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        print("RESUMED")
                        self.resume = True


    def in2Dcenter(self, d2list):
        return [d2list[0]*self.LLSS/2+self.DDSS[0]/2, -d2list[1]*self.LLSS/2+self.DDSS[1]/2 ]
