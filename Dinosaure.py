import numpy as np
from numpy import random
import math

class Dinosaure:
    def __init__(self, rayon,vitesse,position):
        self.rayon = rayon #rayon de courbure minimal de sa trajectoire
        self.vitesse = vitesse/3.6 # vitesse maximale du dinosaure input en km/h, convertie directement en m/s
        self.position = position # position actuelle du dinosaure
        self.lastPosition = np.array([0,0]) ## dernière position, pour calculer la direction. Initialisée à (0,0) ??
        self.direction = np.subtract(self.position, self.lastPosition) # direction actuelle du dinosaure


    def __str__(self):
        return "**** Dinosaure: rayon: %.1f m, vitesse max : %.2f m/s = %.2f km/h \n     Position actuelle : %s , direction : %s" \
               % (self.rayon,self.vitesse,3.6*self.vitesse,self.position,self.direction)

    def seDeplacer(self,destination,dt):
        cible = np.subtract(destination,self.position)
        # deviation = np.arctan2(cible[1], cible[0]) - np.arctan2(self.direction[1], self.direction[0]);

        plusOuMoins = np.sign(np.linalg.det(np.array([cible,self.direction])))
        deviation = plusOuMoins * np.arccos(np.dot(cible,self.direction)/(np.linalg.norm(cible)*np.linalg.norm(self.direction)))

        signe = plusOuMoins
        # si la cible se trouve dans l'un des cercles autour du dinosaure, il faut tourner autour de l'autre
        # cercle. Note: ici c'est pas ça, le centre n'est pas la position du dino. !!!! plus tard
        if (destination[0] - self.centre(signe)[0])**2 + (destination[1] - self.centre(signe)[1])**2 <= self.rayon**2:
            print("***** attention cible proche, possibilité de changer de cercle ***")
            print("centre + ",self.centre(1))
            print("centre - ",self.centre(-1))
            print("destination",destination)
            self.rotate(-signe,dt)

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
            print("centre choisi",np.array([ox,oy]))
            angle = -signe*self.vitesse*dt/r

            #Rotation du point
            PX = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            PY = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            self.position = np.array([PX,PY])

            #Rotation du vecteur
            DX = math.cos(angle) * (dx) - math.sin(angle) * (dy)
            DY = math.sin(angle) * (dx) + math.cos(angle) * (dy)
            self.direction = np.array([DX,DY])

    def translate(self,dt): # se déplacer tout droit à vitesse constante
        self.lastPosition = self.position.copy()
        self.position = np.add(self.position, np.multiply(self.vitesse*dt, self.direction))
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
