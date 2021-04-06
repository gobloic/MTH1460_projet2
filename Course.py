from sympy import *
from sympy.geometry import *
from sympy.plotting import plot
import numpy as np
import math

from Dinosaure import Dinosaure

import matplotlib.pyplot as plt
import matplotlib.animation as animation

dinosaure1 = Dinosaure(0.5,50,np.array([0,0]))
dinosaure2 = Dinosaure(1.5,60,np.array([-10,0]))

dinosaure3 = Dinosaure(1.5,60,np.array([10,20]))

# dinosaure1.direction = dinosaure1.position - dinosaure2.position
dinosaure1.direction = dinosaure1.position - dinosaure2.position
dinosaure1.direction = dinosaure1.direction/(np.linalg.norm(dinosaure1.direction))
dinosaure2.direction = dinosaure1.position - dinosaure2.position
dinosaure2.direction = dinosaure2.direction/(np.linalg.norm(dinosaure2.direction))
dinosaure3.direction = dinosaure1.position - dinosaure3.position
dinosaure3.direction = dinosaure3.direction/(np.linalg.norm(dinosaure3.direction))

print(dinosaure1)

xPos = [dinosaure1.getX()]
yPos = [dinosaure1.getY()]
xPos2 = [dinosaure2.getX()]
yPos2 = [dinosaure2.getY()]
xPos3 = [dinosaure3.getX()]
yPos3 = [dinosaure3.getY()]
vit1 = [np.linalg.norm(dinosaure1.direction)]


# destination = np.array([1.5,50])

separationVec = [np.linalg.norm(dinosaure1.position - dinosaure2.position)]

angle = []

tmax = 15
t = 0
dt = 0.01
destination = dinosaure1.position + 1000*(-dinosaure2.position + dinosaure1.position)
distanceDecision = 2
rayonCapture = 0.2
anticipation = 2
compteur = 0
event = 0

delai = -1

# dépend de la statégie, peut valoir 90,180,270 ... au besoin
angleVirageProie = np.radians(45)
tempsProcedure = np.round(angleVirageProie*2*dinosaure1.rayonMin/(dinosaure1.vitesse*dt))
print("tpsProce",tempsProcedure)
signeFixe = 1.0
while (t<tmax):
    print("---")
    t += dt
    dinosaure1.iterationsAvantFinVirage -= 1
    delai -= 1
    print(dinosaure1.iterationsAvantFinVirage)


    if (dinosaure1.iterationsAvantFinVirage < 0) and np.linalg.norm(dinosaure1.position - dinosaure2.position) <= distanceDecision:  # (np.linalg.norm(dinosaure1.position - dinosaure3.position) <= distanceDecision) or
        # destination = dinosaure1.position + 1000*np.array([-dinosaure1.direction[1],dinosaure1.direction[0]])
        dinosaure1.iterationsAvantFinVirage = tempsProcedure
        delai = 200

    if dinosaure1.iterationsAvantFinVirage > 0:
        destination = dinosaure1.position + 1000*np.array([-dinosaure1.direction[1],dinosaure1.direction[0]])
    else :
        destination = dinosaure1.position + 1000 * dinosaure1.direction  # + 1000*(dinosaure1.position - dinosaure2.position )




    # destination = 2*dinosaure1.position - dinosaure2.position

    # print(np.linalg.norm(dinosaure1.direction))
    # declencheur =  (np.linalg.norm(dinosaure1.position - dinosaure2.position) <= distanceDecision) # (np.linalg.norm(dinosaure1.position - dinosaure3.position) <= distanceDecision) or
    # if declencheur:
    #     if compteur <= 0:
    #         compteur = tempsProcedure
    #     # print("l'évènenement déclencheur a lieu")
    #     event += 1
    #     firstTime = (event == 1)
    #     if firstTime:
    #         # print("c'est la première fois, il faut changer. La procédure va durer ",tempsProcedure," itérations")
    #         compteur = tempsProcedure
    #         signeFixe = (2*np.round(np.random.rand())-1)
    #         destination = dinosaure1.position + signeFixe\
    #                       *1000*np.array([-dinosaure1.direction[1],dinosaure1.direction[0]])
    #     else:
    #         compteur -= 1
    #         # print("c'est pas la première fois, ne fais rien. Ce sera le cas pour encore ",compteur, " itérations")
    # else:
    #     if compteur > 0:
    #         compteur -= 1
    #         # print("l'événement déclencheur n'a pas lieu mais il reste du temps à la procédure : ", compteur)
    #         destination = dinosaure1.position + signeFixe \
    #                       *1000*np.array([-dinosaure1.direction[1],dinosaure1.direction[0]])
    #
    #     else:
    #         # destination = 2*dinosaure1.position - dinosaure2.position
    #         event = 0
    #         compteur = tempsProcedure
    # # print(destination)


    #
    # # destination de la proie instinctive : opposé à la position du prédateur par rapport à la proie
    # destination = dinosaure1.position + 1000* (2*dinosaure1.position - dinosaure3.position - dinosaure2.position)
    # # si le prédateur est trop proche, prendre la décision de changer de direction
    # if np.linalg.norm(dinosaure1.position - dinosaure2.position) < distanceDecision:
    #     destination = dinosaure1.position + 1000*np.array([-dinosaure1.direction[1],dinosaure1.direction[0]])
    #



    # dinosaure1 (proie) se déplace à destination de sa destination
    dinosaure1.seDeplacer(destination,dt)

    # si la proie est dans le rayon de captue du prédateur, elle se fait manger. fin de la simulation
    if (np.linalg.norm(dinosaure2.position - dinosaure1.position) <= rayonCapture) or (np.linalg.norm(dinosaure3.position - dinosaure1.position) <= rayonCapture):
        print("crounch")
        # tfinal = t
        # print('tfinal',tfinal,'tmax',tmax)
        # break


    # ici, décommenter ce que tu veux pour différentes stratégies

    ## proie suicidaire : essaie de se déplacer vers l'arrière du prédateur
    # dinosaure1.seDeplacer(dinosaure2.position - dinosaure2.vitesse*dt*dinosaure2.direction,dt)
    ## prédateur instinctif : se déplace vers la proie
    dinosaure2.seDeplacer(dinosaure1.position,dt)
    # dinosaure3.seDeplacer(dinosaure1.position,dt)
    ## prédateur prédictif : anticipe
    # dinosaure2.seDeplacer(dinosaure1.position + anticipation*dinosaure1.direction*dinosaure1.vitesse*dt,dt)


    xPos.append(dinosaure1.getX())
    yPos.append(dinosaure1.getY())
    xPos2.append(dinosaure2.getX())
    yPos2.append(dinosaure2.getY())
    xPos3.append(dinosaure3.getX())
    yPos3.append(dinosaure3.getY())
    vit1.append(np.linalg.norm(dinosaure1.direction))
    separationVec.append(np.linalg.norm(dinosaure1.position - dinosaure2.position))






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

    # Attach 3D axis to the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    data = np.array([np.vstack((xPos, yPos))])
    data2 = np.array([np.vstack((xPos2, yPos2))])
    data3 = np.array([np.vstack((xPos3, yPos3))])

    n=int(np.round(tmax/dt))
    # Create line objects:
    auv = [ax.plot(data[0][0,0:2], data[0][1,0:2],  'ro')[0]]
    trj = [ax.plot(data[0][0,0:2], data[0][1,0:2],'+r')[0]]

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


    # ####### show result
    #
    # fig = plt.figure()
    # plt.plot(data[0][0,0:2], data[0][1,0:2],':r')
    # plt.show()



    # Creating the Animation object
    ani_auv = animation.FuncAnimation(fig, update_auv, n, fargs=(data, auv),
                                      interval=n/100, blit=False, repeat=False) #repeat=False,
    ani_trj = animation.FuncAnimation(fig, update_trj, n, fargs=(data, trj),
                                      interval=n/100, blit=False, repeat=False) #repeat=False,

    ani_auv2 = animation.FuncAnimation(fig, update_auv, n, fargs=(data2, auv2),
                                      interval=n/100, blit=False, repeat=False) #repeat=False,
    ani_trj2 = animation.FuncAnimation(fig, update_trj, n, fargs=(data2, trj2),
                                      interval=n/100, blit=False, repeat=False) #repeat=False,

    ani_auv3 = animation.FuncAnimation(fig, update_auv, n, fargs=(data3, auv3),
                                       interval=n/100, blit=False, repeat=False) #repeat=False,
    ani_trj3 = animation.FuncAnimation(fig, update_trj, n, fargs=(data3, trj3),
                                       interval=n/100, blit=False, repeat=False) #repeat=False,

    plt.show()
    # fig.savefig("./figures/testDroiteHorsCercle.png", dpi=600)


    # fig = plt.figure()
    # plt.plot(separationVec,"+")
    #
    # plt.plot(distanceDecision*np.ones(len(separationVec)),'r')
    # plt.plot(rayonCapture*np.ones(len(separationVec)),'b')
    # plt.show()
