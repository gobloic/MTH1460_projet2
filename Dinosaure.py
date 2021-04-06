import numpy as np
from numpy import random
import math

class Dinosaure:
    def __init__(self, rayonMin,vitesse,position):
        self.rayonMin = rayonMin #rayon de courbure minimal de sa trajectoire
        self.vitesse = vitesse/3.6 # vitesse maximale du dinosaure input en km/h, convertie directement en m/s
        self.position = position # position actuelle du dinosaure
        self.lastPosition = np.array([0,0]) ## dernière position, pour calculer la direction. Initialisée à (0,0) ??
        self.direction = np.subtract(self.position, self.lastPosition) # direction actuelle du dinosaure
        self.rayon = rayonMin
        self.iterationsAvantFinVirage = -1


    def __str__(self):
        return "**** Dinosaure: rayon: %.1f m, vitesse max : %.2f m/s = %.2f km/h \n     Position actuelle : %s , direction : %s" \
               % (self.rayon,self.vitesse,3.6*self.vitesse,self.position,self.direction)

    def seDeplacer(self,destination,dt):
        cible = destination - self.position
        plusOuMoins = np.sign(np.linalg.det(np.array([cible,self.direction])))
        deviation = plusOuMoins * np.arccos(np.dot(cible,self.direction)/(np.linalg.norm(cible)*np.linalg.norm(self.direction)))
        angleMax = 1/2 * self.vitesse*dt/self.rayonMin;
        signe = plusOuMoins

        if np.abs(deviation) < angleMax:
            if deviation == 0:
                print("tout droit!!")
                signe = 0
                if np.dot(cible,self.direction) < 0:
                    signe = -1;
            else:
                self.rayon = 1/2 * self.vitesse*dt/np.abs(deviation)
            # print("rayon rotation",self.rayon)
            self.rotate(signe,dt)
            # print (np.subtract(destination,self.position)/np.linalg.norm(np.subtract(destination,self.position)) - self.direction/np.linalg.norm(self.direction))
        else:
            self.rayon = self.rayonMin
            # print("rayon rotation",self.rayon)

            # si la cible se trouve dans l'un des cercles autour du dinosaure, il faut tourner autour de l'autre
            # cercle. c'est bon ça marche comme je veux :)
            centrePlus = self.centre(+1)
            centreMoins = self.centre(-1)
            if (np.linalg.norm(centrePlus-destination))**2 <= self.rayon**2 or (np.linalg.norm(centreMoins-destination))**2 <= self.rayon**2:
                print("BBBBBB*********")
                if (np.linalg.norm(centrePlus-destination))**2 <= self.rayon**2:
                    signe = -1
                if (np.linalg.norm(centreMoins-destination))**2 <= self.rayon**2:
                    signe = +1

            if deviation == 0:
                signe = 0
            # si les deux vecteurs sont colinéaires, regarder si ils sont de même sens ou pas
            if signe == 0:
                if np.dot(cible,self.direction) < 0:
                    signe = -1;
            self.rotate(signe,dt)

    def centre(self,signe):
        px,py = self.position
        dx,dy = self.direction
        r = self.rayon
        ox = px + signe*r*dy
        oy = py - signe*r*dx
        return np.array([ox,oy])

    ## signe - : tourner vers la droite // signe + : tourner vers la gauche
    def rotate(self,signe,dt): # tourner en un incrément de temps
        if signe == 0:
            self.translate(dt)
        else:
            self.lastPosition = self.position.copy()
            px,py = self.position
            dx,dy = self.direction
            r = self.rayon
            ox,oy = self.centre(signe)
            # print("centre choisi",np.array([ox,oy]))
            angle = -signe*self.vitesse*dt/r

            #Rotation du point
            PX = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            PY = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            self.position = np.array([PX,PY])

            #Rotation du vecteur
            DX = math.cos(angle) * (dx) - math.sin(angle) * (dy)
            DY = math.sin(angle) * (dx) + math.cos(angle) * (dy)
            self.direction = np.array([DX,DY])
            self.direction = self.direction/np.linalg.norm(self.direction)

    def translate(self,dt): # se déplacer tout droit à vitesse constante
        self.lastPosition = self.position.copy()
        self.position = self.position + self.direction/np.linalg.norm(self.direction) * (self.vitesse*dt)
        print("**translate")

    def getX(self):
        return self.position[0]
    def getY(self):
        return self.position[1]
    def setX(self,x):
        self.position[0] = x
    def setY(self,y):
        self.position[1] = y
    def getDirectionX(self):
        return self.direction[0]
    def getDirectionY(self):
        return self.direction[1]
