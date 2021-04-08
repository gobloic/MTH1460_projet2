import numpy as np
from numpy import random
import math

from Dinosaure import Dinosaure




class Thescelosaurus(Dinosaure):

    def __init__(self,position):
        super().__init__(0.5,50,position)
        self.isTurning = False
        self.signeFixe = 1.0
        self.destination = self.position + 1000*self.direction
        self.compteurTour = 0

    def fuir(self,predateur1,strategie,dt):


        signeFixe=1
        # destination = self.position + self.direction


        if strategie == "naive":
            self.destination = 2*self.position - predateur1.position
            distanceDecision = predateur1.rayonCapture * 3

            if np.linalg.norm(self.position - predateur1.position) <= distanceDecision and not self.isTurning:
                self.rayon = self.rayonMin
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                self.isTurning = True

            if self.isTurning and self.compteurTour < 2*math.pi*self.rayon/(self.vitesse * dt):
                self.rotate(self.signeFixe,dt)
                self.compteurTour += 1
            else:
                self.translate(dt)
                self.compteurTour = 0

        elif strategie == "90":
            distanceDecision = 3.5

            if not self.isTurning:
                self.destination = self.position + 1000*self.direction

            if self.alignedWithDestination() and self.isTurning:
                self.isTurning = False

            if np.linalg.norm(self.position - predateur1.position) <= distanceDecision and not self.isTurning:
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                angleFixe = 90 #180*np.random.rand()
                self.destination = self.newDestination(self.signeFixe*angleFixe)
                # self.isTurning = True
                # predateur1.direction = np.array([0,0]) #arrêter le prédateur pour voir


            self.seDeplacer(dt)



        elif strategie == "faceAFace":
            pass

        elif strategie == "angleAleatoire":
            distanceDecision = 3.5

            if not self.isTurning:
                self.destination = self.position + 1000*self.direction

            if self.alignedWithDestination() and self.isTurning:
                print("ALIGNED")
                self.isTurning = False

            if np.linalg.norm(self.position - predateur1.position) <= distanceDecision and not self.isTurning:
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                angleFixe = 180*np.random.rand()
                self.destination = self.newDestination(self.signeFixe*angleFixe)

            self.seDeplacer(dt)


        else:
            print("strategie inconnue")



    # def fuir(self,predateur1, predateur2):

    def newDestination(self,angle):
        px,py = self.position
        dx,dy = self.direction
        self.rayon = self.rayonMin
        signe = np.sign(angle)
        angle = np.radians(angle)
        ox,oy = self.centre(signe)

        #Rotation du point
        PX = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        PY = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        M = np.array([PX,PY])

        #Rotation du vecteur
        DX = math.cos(angle) * (dx) - math.sin(angle) * (dy)
        DY = math.sin(angle) * (dx) + math.cos(angle) * (dy)
        u = np.array([DX,DY])
        u = u/np.linalg.norm(u)
        print("vecteur u : ",u)
        print("u.d = ", np.dot(u,self.direction))

        return M + 1000*u

    def alignedWithDestination(self):
        return (np.cross(self.direction,self.destination) == 0)

    # override translate pour ajouter l'info que tu n'es plus en train de tourner
    def translate(self,dt):
        self.isTurning = False
        super().translate(dt)

        print("override Translate")

    def rotate(self,signe,dt):
        self.isTurning = True
        super().rotate(signe,dt)

        print("Override Rotate")

    def seDeplacer(self,dt):
        super().seDeplacer(self.destination,dt)