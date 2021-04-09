import numpy as np
import math

from Velociraptor import Velociraptor
from Thescelosaurus import Thescelosaurus
import matplotlib.pyplot as plt
import matplotlib.animation as animation


SMALL_SIZE = 18
MEDIUM_SIZE = 20
BIGGER_SIZE = 24

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


# minimum 15m maximum 42m ? Ziling ?
distanceInitiale = 15 + (42-15) * np.random.rand()
angleInitial = 2*math.pi*np.random.rand()

proie = Thescelosaurus(np.array([10,10]))


# position initiale aléatoire
predateur1 = Velociraptor(np.array([proie.getX() + distanceInitiale*np.cos(angleInitial),proie.getY() +
                                    distanceInitiale*np.sin(angleInitial)]))
# predateur2 = Velociraptor(np.array([10,20]))

crounch = False

proie.direction = proie.position - predateur1.position
proie.direction = proie.direction/(np.linalg.norm(proie.direction))
predateur1.direction = proie.position - predateur1.position
predateur1.direction = predateur1.direction/(np.linalg.norm(predateur1.direction))
# predateur2.direction = proie.position - predateur2.position
# predateur2.direction = predateur2.direction/(np.linalg.norm(predateur2.direction))



xPos = [proie.getX()]
yPos = [proie.getY()]
xPos2 = [predateur1.getX()]
yPos2 = [predateur1.getY()]
# xPos3 = [predateur2.getX()]
# yPos3 = [predateur2.getY()]

separationVec = [np.linalg.norm(proie.position - predateur1.position)]
signeVec = []


tmax = 15
t = 0
dt = 0.01



signeFixe = 1.0
while (t<tmax):
    # print("---")
    t += dt

    # proie fuit le spredateur selon la strategie choisie : "naive","90","faceAFace" (pas encore codé),"angleAleatoire"
    proie.fuir(predateur1,strategie = "90",dt = dt)
    # print("proie.signeFixe",proie.signeFixe)

    ## prédateur instinctif : se déplace vers la proie
    predateur1.poursuivre(proie,anticipation = 3,dt = dt)


    # si la proie est dans le rayon de captue du prédateur, elle se fait manger. fin de la simulation
    if (np.linalg.norm(predateur1.position - proie.position) <= predateur1.rayonCapture) : #or\
        # (np.linalg.norm(predateur2.position - proie.position) <= predateur2.rayonCapture):
        print("crounch")
        crounch = True
        # tfinal = t
        # print('tfinal',tfinal,'tmax',tmax)
        break


    xPos.append(proie.getX())
    yPos.append(proie.getY())
    xPos2.append(predateur1.getX())
    yPos2.append(predateur1.getY())
    # xPos3.append(predateur2.getX())
    # yPos3.append(predateur2.getY())
    separationVec.append(np.linalg.norm(proie.position - predateur1.position))


if crounch:
    print("La proie a été mangée après ", t, " s")
else:
    print("La proie s'est échappée après ",t," s")






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
    # data3 = np.array([np.vstack((xPos3, yPos3))])

    # first print the final result
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if crounch:
        state = " la proie est attrapée après %.2f secondes"%(t)
    else:
        state = " la proie s'est enfuie"

    title = 'Trajectoires finales : ' + state +"\n Distance initiale : %.2f m"%(distanceInitiale)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.set_xlim([min(1.15*min(data[0,0,:]),1.15*min(data2[0,0,:])), max(1.15*max(data[0,0,:]),1.15*max(data2[0,0,:]))])
    ax.set_ylim([min(1.15*min(data[0,1,:]),1.15*min(data2[0,1,:])), max(1.15*max(data[0,1,:]),1.15*max(data2[0,1,:]))])
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')



    ax.plot(data[0,0,:],data[0,1,:],'r',label="Thescelosaurus (proie)")
    ax.plot(data2[0,0,:],data2[0,1,:],'b',label="Velociraptor (prédateur)")
    # ax.plot(data3[0,0,:],data3[0,1,:],'-+b')

    plt.get_current_fig_manager().window.state('zoomed')
    plt.legend()
    plt.show()
    fig.savefig("./figures/crounch%sstrategie90.png"%(crounch), dpi=600)

    # Attach 3D axis to the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    n=int(np.round(tmax/dt))
    # Create line objects:
    auv = [ax.plot(data[0][0,0:2], data[0][1,0:2],  'ro',label="Thescelosaurus (proie)")[0]] #markersize = 30
    trj = [ax.plot(data[0][0,0:2], data[0][1,0:2],'r')[0]]

    auv2 = [ax.plot(data2[0][0,0:2], data2[0][1,0:2],   marker=(5, 2),color='b',label = "Velociraptor (prédateur)")[0]]
    trj2 = [ax.plot(data2[0][0,0:2], data2[0][1,0:2],'b')[0]]
    #
    # auv3 = [ax.plot(data3[0][0,0:2], data3[0][1,0:2],   marker=(4,2),color='b')[0]]
    # trj3 = [ax.plot(data3[0][0,0:2], data3[0][1,0:2],'b')[0]]


    # Setthe axes properties
    # ,1.15*min(data3[0,0,:]) // ,1.15*max(data3[0,0,:])
    ax.set_xlim([min(1.15*min(data[0,0,:]),1.15*min(data2[0,0,:])), max(1.15*max(data[0,0,:]),1.15*max(data2[0,0,:]))])
    ax.set_xlabel('x (m)')

    # ,1.15*min(data3[0,1,:]) // ,1.15*max(data3[0,1,:])
    ax.set_ylim([min(1.15*min(data[0,1,:]),1.15*min(data2[0,1,:])), max(1.15*max(data[0,1,:]),1.15*max(data2[0,1,:]))])
    ax.set_ylabel('y (m)')

    ax.set_axis_off()

    # ax.set_title('2D Test')


    interval = 2
    frames = n


    # Creating the Animation object
    ani_auv = animation.FuncAnimation(fig, update_auv, frames = frames, fargs=(data, auv),
                                      interval=interval, blit=False, repeat=False) #repeat=False,
    ani_trj = animation.FuncAnimation(fig, update_trj, frames = frames, fargs=(data, trj),
                                      interval=interval, blit=False, repeat=False) #repeat=False,

    ani_auv2 = animation.FuncAnimation(fig, update_auv,frames = frames, fargs=(data2, auv2),
                                      interval=interval, blit=False, repeat=False) #repeat=False,
    ani_trj2 = animation.FuncAnimation(fig, update_trj,frames = frames, fargs=(data2, trj2),
                                      interval=interval, blit=False, repeat=False) #repeat=False,

    # ani_auv3 = animation.FuncAnimation(fig, update_auv,frames = frames, fargs=(data3, auv3),
    #                                    interval=interval, blit=False, repeat=False) #repeat=False,
    # ani_trj3 = animation.FuncAnimation(fig, update_trj,frames = frames, fargs=(data3, trj3),
    #                                    interval=interval, blit=False, repeat=False) #repeat=False,

    plt.get_current_fig_manager().window.state('zoomed')
    plt.legend()
    plt.show()




