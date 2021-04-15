import numpy as np
from numpy import random

from Dinosaure import Dinosaure

class Velociraptor(Dinosaure):
    def __init__(self,position):
        super().__init__(6,60,position)
        self.rayonCapture = 1.5
        self.attack = False


    def poursuivre(self,proie,anticipation,dt):
        super().seDeplacer(proie.position + anticipation*proie.direction*proie.vitesse*dt,dt)

    def attendre(self,proie,dt):
        if proie.isTurning:
            self.attack = True
        else:
            self.attack = False

        if self.attack:
            super().seDeplacer(proie.position,dt)
        else:
            super().seDeplacer(self.position - proie.direction*proie.vitesse*dt,dt)



