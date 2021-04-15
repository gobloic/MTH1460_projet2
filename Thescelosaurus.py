import numpy as np
from numpy import random
import math

from Dinosaure import Dinosaure




class Thescelosaurus(Dinosaure):

    def __init__(self,position):
        super().__init__(2,50,position)
        self.isTurning = False
        self.signeFixe = 1.0
        self.destination = self.position + 1000*self.direction
        self.compteurTour = 0
        self.feintAndBluff = False

    def fuir1(self,predateur1,strategie,dt):

        if strategie == "naive":
            self.destination = 2*self.position - predateur1.position
            self.seDeplacer(dt)

        elif strategie == "90":
            distanceDecision = 6

            # tant que c'est suffisant, courir tout droit
            if not self.isTurning:
                self.destination = self.position + 1000*self.direction

            # si le prédateur entre dans la zone, entamer un virage à 90°
            if np.linalg.norm(self.position - predateur1.position) <= distanceDecision and not self.isTurning:
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                angleFixe = 90
                self.destination = self.newDestination(self.signeFixe*angleFixe)

            self.seDeplacer(dt)

            # si la manoeuvre est terminée, courir tout droit de nouveau
            if self.alignedWithDestination():
                self.isTurning = False

        elif strategie == "faceAFace":
            distanceDecision1 = 15
            distanceDecision2 = 10

            if not self.isTurning:
                self.destination = self.position + 1000*(self.direction)


            if np.linalg.norm(self.position - predateur1.position) <= distanceDecision1 and not self.isTurning \
                    and not self.feintAndBluff:
                self.destination = predateur1.position


            if np.linalg.norm(self.position - predateur1.position) <= distanceDecision2 and not self.isTurning \
                    and not self.feintAndBluff:
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                angleFixe = 90
                self.destination = self.newDestination(self.signeFixe*angleFixe)
                self.feintAndBluff = True

            if not self.feintAndBluff:
                self.seDeplacer(dt)
            else:
                signe = np.sign(np.linalg.det(np.array([predateur1.position - self.position,self.direction])))
                angleFixe = 180
                self.compteurTour += 1
                if self.compteurTour < np.radians(angleFixe)/2*self.rayon/(self.vitesse * dt):
                    self.rotate(-signe,dt)
                elif (np.radians(angleFixe)/2*self.rayon/(self.vitesse * dt) <= self.compteurTour
                    < np.radians(angleFixe)*self.rayon/(self.vitesse * dt)):
                    self.rotate(signe,dt)
                else:
                    self.translate(dt)
                    if self.compteurTour > 100:
                        self.feintAndBluff = False
                        self.compteurTour = 0


            if self.alignedWithDestination():
                self.isTurning = False

        elif strategie == "angleAleatoire":
            distanceDecision = 6

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


    # adaptation des stratégies de fuite pour deux prédateurs (majoritairement du copié/collé de fuir1)
    def fuir2(self,predateur1, predateur2,strategie,dt):

        if strategie == "naive":
            self.destination = self.position + 1000*(2*self.position - predateur1.position - predateur2.position)
            self.seDeplacer(dt)

        elif strategie == "90":
            distanceDecision = 6

            if not self.isTurning:
                self.destination = self.position + 1000*self.direction


            if ((np.linalg.norm(self.position - predateur1.position) <= distanceDecision) or
                ((np.linalg.norm(self.position - predateur2.position) <= distanceDecision))) \
                    and not self.isTurning:
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                angleFixe = 90
                self.destination = self.newDestination(self.signeFixe*angleFixe)

            self.seDeplacer(dt)

            if self.alignedWithDestination():
                self.isTurning = False

        elif strategie == "angleAleatoire":
            distanceDecision = 6

            if not self.isTurning:
                self.destination = self.position + 1000*self.direction

            if self.alignedWithDestination() and self.isTurning:
                print("ALIGNED")
                self.isTurning = False

            if ((np.linalg.norm(self.position - predateur1.position) <= distanceDecision) or
                ((np.linalg.norm(self.position - predateur2.position) <= distanceDecision))) \
                    and not self.isTurning:
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                angleFixe = 180*np.random.rand()
                self.destination = self.newDestination(self.signeFixe*angleFixe)

            self.seDeplacer(dt)

        elif strategie == "faceAFace":
            distanceDecision1 = 15
            distanceDecision2 = 10

            if not self.isTurning:
                self.destination = self.position + 1000*(self.direction)


            if ((np.linalg.norm(self.position - predateur1.position) <= distanceDecision1) or
                ((np.linalg.norm(self.position - predateur2.position) <= distanceDecision1))) \
                    and not self.isTurning and not self.feintAndBluff:
                if np.linalg.norm(self.position - predateur1.position) <= distanceDecision1:
                    self.destination = predateur1.position
                    self.predateurAFeinter = predateur1
                elif np.linalg.norm(self.position - predateur2.position) <= distanceDecision1:
                    self.destination = predateur2.position
                    self.predateurAFeinter = predateur2


            if ((np.linalg.norm(self.position - predateur1.position) <= distanceDecision2) or
                ((np.linalg.norm(self.position - predateur2.position) <= distanceDecision2))) \
                    and not self.isTurning and not self.feintAndBluff:
                self.signeFixe = 2*np.round(np.random.rand()) - 1
                angleFixe = 90
                self.destination = self.newDestination(self.signeFixe*angleFixe)
                self.feintAndBluff = True

            if not self.feintAndBluff:
                self.seDeplacer(dt)
            else:
                angleFixe = 180
                signe = np.sign(np.linalg.det(np.array([self.predateurAFeinter.position - self.position,self.direction])))
                self.compteurTour += 1
                if self.compteurTour < np.radians(angleFixe)/2*self.rayon/(self.vitesse * dt):
                    self.rotate(-signe,dt)
                elif (np.radians(angleFixe)/2*self.rayon/(self.vitesse * dt) <= self.compteurTour
                      < np.radians(angleFixe)*self.rayon/(self.vitesse * dt)):
                    self.rotate(signe,dt)
                else:
                    self.translate(dt)
                    if self.compteurTour > 100:
                        self.feintAndBluff = False
                        self.compteurTour = 0


            if self.alignedWithDestination():
                self.isTurning = False




    # méthode qui met à jour la destination du dinosaure à un point lointain qui lui permet de dévier sa trajectoire
    # d'un angle prédéfini

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

        return M + 1000*u

    def alignedWithDestination(self):
        return (np.cross(self.direction,self.destination) == 0)

    # override translate de Dinosaure pour ajouter l'info que tu n'es plus en train de tourner
    def translate(self,dt):
        self.isTurning = False
        super().translate(dt)

    def rotate(self,signe,dt):
        self.isTurning = True
        super().rotate(signe,dt)

    def seDeplacer(self,dt):
        super().seDeplacer(self.destination,dt)