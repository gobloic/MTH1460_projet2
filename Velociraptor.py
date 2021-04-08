import numpy as np
from numpy import random

from Dinosaure import Dinosaure

class Velociraptor(Dinosaure):
    def __init__(self,position):
        super().__init__(1.5,60,position)
        self.rayonCapture = 0.6 #ref : A4


    def poursuivre(self,proie,anticipation,dt):
        super().seDeplacer(proie.position + anticipation*proie.direction*proie.vitesse*dt,dt)



