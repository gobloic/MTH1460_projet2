from sympy import *
from sympy.geometry import *
from sympy.plotting import plot
import numpy as np
import math

from Velociraptor import Velociraptor
from Thescelosaurus import Thescelosaurus

import matplotlib.pyplot as plt
import matplotlib.animation as animation

proie = Thescelosaurus(np.array([0,0]))
predateur1 = Velociraptor(np.array([10,0]))

predateur2 = Velociraptor(np.array([10,20]))

# proie.direction = proie.position - predateur1.position
proie.direction = proie.position - predateur1.position
proie.direction = proie.direction/(np.linalg.norm(proie.direction))
predateur1.direction = proie.position - predateur1.position
predateur1.direction = predateur1.direction/(np.linalg.norm(predateur1.direction))
predateur2.direction = proie.position - predateur2.position
predateur2.direction = predateur2.direction/(np.linalg.norm(predateur2.direction))



xPos = [proie.getX()]
yPos = [proie.getY()]
xPos2 = [predateur1.getX()]
yPos2 = [predateur1.getY()]
xPos3 = [predateur2.getX()]
yPos3 = [predateur2.getY()]
vit1 = [np.linalg.norm(proie.direction)]


# destination = np.array([1.5,50])

separationVec = [np.linalg.norm(proie.position - predateur1.position)]

angle = []

tmax = 15
t = 0
dt = 0.01
# destination = proie.position + 1000*(-predateur1.position + proie.position)
destination = np.array([0,1000])
distanceDecision = 2
anticipation = 2




signeFixe = 1.0
while (t<tmax):
    print("---")
    t += dt

    # proie fuit le spredateur selon la strategie choisie : "naive","90","faceAFace" (pas encore codé),"angleAleatoire"
    proie.fuir(predateur1,strategie = "90",dt = dt)




    # ici, décommenter ce que tu veux pour différentes stratégies

    ## proie suicidaire : essaie de se déplacer vers l'arrière du prédateur
    # proie.seDeplacer(predateur1.position - predateur1.vitesse*dt*predateur1.direction,dt)
    ## prédateur instinctif : se déplace vers la proie
    predateur1.poursuivre(proie,anticipation = 0,dt = dt)
    # predateur2.seDeplacer(proie.position,dt)
    ## prédateur prédictif : anticipe
    # predateur1.seDeplacer(proie.position + anticipation*proie.direction*proie.vitesse*dt,dt)


    # si la proie est dans le rayon de captue du prédateur, elle se fait manger. fin de la simulation
    if (np.linalg.norm(predateur1.position - proie.position) <= predateur1.rayonCapture) or (np.linalg.norm(predateur2.position - proie.position) <= predateur2.rayonCapture):
        print("crounch")
        # tfinal = t
        # print('tfinal',tfinal,'tmax',tmax)
        # break


    xPos.append(proie.getX())
    yPos.append(proie.getY())
    xPos2.append(predateur1.getX())
    yPos2.append(predateur1.getY())
    xPos3.append(predateur2.getX())
    yPos3.append(predateur2.getY())
    vit1.append(np.linalg.norm(proie.direction))
    separationVec.append(np.linalg.norm(proie.position - predateur1.position))






############################################################################
##############################  GRAPHIQUES #################################
############################################################################

if True:

    # Update AUV position for plotting:
    def update_auv(num, dataLines, lines) :
        for line, data in zip(lines, dataLines) :
            line.set_data(data[0:2, num-1:num])
            # line.set_properties(data[1,num-1:num])
        return lines

    # Update trajectory for plotting:
    def update_trj(num, dataLines, lines) :
        for line, data in zip(lines, dataLines) :
            line.set_data(data[0:2, :num])
            # line.set_properties(data[1,:num])
        return lines
    ###############################################################################



    data = np.array([np.vstack((xPos, yPos))])
    data2 = np.array([np.vstack((xPos2, yPos2))])
    data3 = np.array([np.vstack((xPos3, yPos3))])

    # first print the final result
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_title('Trajectoires finales')
    ax.set_aspect('equal')
    ax.plot(data[0,0,:],data[0,1,:],'r')
    ax.plot(data2[0,0,:],data2[0,1,:],'b')
    ax.plot(data3[0,0,:],data3[0,1,:],'b')

    plt.show()

    # Attach 3D axis to the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    n=int(np.round(tmax/dt))
    # Create line objects:
    auv = [ax.plot(data[0][0,0:2], data[0][1,0:2],  'ro')[0]] #markersize = 30
    trj = [ax.plot(data[0][0,0:2], data[0][1,0:2],':r')[0]]

    auv2 = [ax.plot(data2[0][0,0:2], data2[0][1,0:2],   marker=(5, 2),color='b')[0]]
    trj2 = [ax.plot(data2[0][0,0:2], data2[0][1,0:2],':b')[0]]

    auv3 = [ax.plot(data3[0][0,0:2], data3[0][1,0:2],   marker=(4,2),color='b')[0]]
    trj3 = [ax.plot(data3[0][0,0:2], data3[0][1,0:2],':b')[0]]

    # ax.plot(0,300,'xr')
    # ax.plot(destination[0],destination[1],'xr')

    #
    # circle1 = plt.Circle((0.5, 0), 0.5, color='r',alpha=0.5)
    # circle2 = plt.Circle((-0.5, 0), 0.5, color='b',alpha=0.5)
    # ax.add_patch(circle1)
    # ax.add_patch(circle2)


    # Setthe axes properties
    ax.set_xlim([min(1.15*min(data[0,0,:]),1.15*min(data2[0,0,:]),1.15*min(data3[0,0,:])), max(1.15*max(data[0,0,:]),1.15*max(data2[0,0,:]),1.15*max(data3[0,0,:]))])
    ax.set_xlabel('X')

    ax.set_ylim([min(1.15*min(data[0,1,:]),1.15*min(data2[0,1,:]),1.15*min(data3[0,1,:])), max(1.15*max(data[0,1,:]),1.15*max(data2[0,1,:]),1.15*max(data3[0,1,:]))])
    ax.set_ylabel('Y')

    # ax.set_ylim([-1,2])
    # ax.set_xlim([-1.5,1.5])
    # ax.set_axis_off()

    # ax.set_zlim3d([-1.0, 1.0])
    # ax.set_zlabel('Z')

    # ax.set_title('2D Test')






    # Creating the Animation object
    ani_auv = animation.FuncAnimation(fig, update_auv, n, fargs=(data, auv),
                                      interval=1, blit=False, repeat=False) #repeat=False,
    ani_trj = animation.FuncAnimation(fig, update_trj, n, fargs=(data, trj),
                                      interval=1, blit=False, repeat=False) #repeat=False,

    ani_auv2 = animation.FuncAnimation(fig, update_auv, n, fargs=(data2, auv2),
                                      interval=1, blit=False, repeat=False) #repeat=False,
    ani_trj2 = animation.FuncAnimation(fig, update_trj, n, fargs=(data2, trj2),
                                      interval=1, blit=False, repeat=False) #repeat=False,

    ani_auv3 = animation.FuncAnimation(fig, update_auv, n, fargs=(data3, auv3),
                                       interval=1, blit=False, repeat=False) #repeat=False,
    ani_trj3 = animation.FuncAnimation(fig, update_trj, n, fargs=(data3, trj3),
                                       interval=1, blit=False, repeat=False) #repeat=False,

    plt.show()
    # fig.savefig("./figures/testDroiteHorsCercle.png", dpi=600)

    #
    # fig = plt.figure()
    # plt.plot(angle,"+")
    #
    # # plt.plot(distanceDecision*np.ones(len(separationVec)),'r')
    # # plt.plot(rayonCapture*np.ones(len(separationVec)),'b')
    # plt.show()
    #

