import numpy as np
from numpy import random

from Dinosaure import Dinosaure

class Velociraptor(Dinosaure):
    def __init__(self,position):
        #accélérations de 20g : 1.5m // accélération de 4.72g : 6 m
        super().__init__(6,60,position)
        self.rayonCapture = 1.5 #1.5 #on peut le changer. Mais c'est le


    def poursuivre(self,proie,anticipation,dt):
        super().seDeplacer(proie.position + anticipation*proie.direction*proie.vitesse*dt,dt)



