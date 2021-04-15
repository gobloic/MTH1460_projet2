import numpy as np
import math

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


from Velociraptor import Velociraptor
from Thescelosaurus import Thescelosaurus

print("### DEBUT DES 300 SIMULATIONS")
nombreSimulations = 300
nombrePredateurs = 2
predateurIntelligent = True
graphiques = True

# proie fuit le spredateur selon la strategie choisie : "naive","90","angleAleatoire","faceAFace"
strategie = "90"

# anticipation du prédateur1:
anticipation = 10

result = []
for simu in range(nombreSimulations):

    # minimum 15m maximum 42m
    distanceInitiale1 = 15 + (42-15) * np.random.rand()
    angleInitial1 = 2*math.pi*np.random.rand()
    distanceInitiale2 = distanceInitiale1
    angleInitial2 = angleInitial1 + math.pi/2 + math.pi/2*np.random.rand()

    proie = Thescelosaurus(np.array([10,10]))


    # position initiale aléatoire autour de la proie
    predateur1 = Velociraptor(np.array([proie.getX() + distanceInitiale1*np.cos(angleInitial1),proie.getY() +
                                        distanceInitiale1*np.sin(angleInitial1)]))
    predateur2 = Velociraptor(np.array([proie.getX() + distanceInitiale2*np.cos(angleInitial2),proie.getY() +
                                        distanceInitiale2*np.sin(angleInitial2)]))

    # critère d'arrêt
    crounch = False

    # réglage initial des directions
    if nombrePredateurs == 1:
        proie.direction = proie.position - predateur1.position
    elif nombrePredateurs == 2:
        proie.direction = 2*proie.position - predateur1.position - predateur2.position

    proie.direction = proie.direction/(np.linalg.norm(proie.direction))
    predateur1.direction = proie.position - predateur1.position
    predateur1.direction = predateur1.direction/(np.linalg.norm(predateur1.direction))

    if predateurIntelligent:
        predateur2.direction = proie.direction
    else:
        predateur2.direction = proie.position - predateur2.position
    predateur2.direction = predateur2.direction/(np.linalg.norm(predateur2.direction))


    # initialisation des vecteurs qui stockent les positions
    xPos = [proie.getX()]
    yPos = [proie.getY()]
    xPos2 = [predateur1.getX()]
    yPos2 = [predateur1.getY()]
    xPos3 = [predateur2.getX()]
    yPos3 = [predateur2.getY()]

    separationVec = [np.linalg.norm(proie.position - predateur1.position)]
    signeVec = []

    # durée de la simulation et pas de temps
    tmax = 15
    t = 0
    dt = 0.01



    signeFixe = 1.0




    while (t<tmax):

        t += dt

        # Fuite de la proie avec un ou deux prédateurs avec une stratégie établie
        if nombrePredateurs == 1:
            proie.fuir1(predateur1 = predateur1,strategie = strategie,dt = dt)
        elif nombrePredateurs == 2:
            proie.fuir2(predateur1 = predateur1,predateur2 = predateur2, strategie = strategie,dt = dt)

        ## prédateur 1 prédictif : anticipe les déplacements de la proie
        predateur1.poursuivre(proie,anticipation = anticipation,dt = dt)


        if nombrePredateurs == 2:
            if predateurIntelligent :
                # prédateur 2 intelligent : se déplace parallèlement à la proie jusqu'à ce qu'elle change de direction
                predateur2.attendre(proie,dt)
            else:
                # predateur 2 moins intelligent : adopte la même stratégie que le prédateur 1
                predateur2.poursuivre(proie,anticipation = anticipation,dt = dt)



        # si la proie est dans le rayon de captue du prédateur, elle se fait manger. fin de la simulation

        # le critère d'arrêt de la simulation est différent en fonction du nombre de prédateurs
        if nombrePredateurs == 1:
            critereArretSimulation = (np.linalg.norm(predateur1.position - proie.position) <= predateur1.rayonCapture)
        elif nombrePredateurs == 2:
            critereArretSimulation = ((np.linalg.norm(predateur1.position - proie.position) <= predateur1.rayonCapture)
            or (np.linalg.norm(predateur2.position - proie.position) <= predateur2.rayonCapture))

        if critereArretSimulation :
            # print("crounch")
            crounch = True
            # tfinal = t
            # print('tfinal',tfinal,'tmax',tmax)
            break

        # recensement des données
        xPos.append(proie.getX())
        yPos.append(proie.getY())
        xPos2.append(predateur1.getX())
        yPos2.append(predateur1.getY())
        xPos3.append(predateur2.getX())
        yPos3.append(predateur2.getY())

    # affichage du résultat de la simulation dans la console
    if crounch:
        print("La proie a été mangée après ", t, " s")
        result.append(1)
    else:
        print("La proie s'est échappée après ",t," s")
        result.append(0)

# affichage du résultat après 300 simulations
print("result",result)
print("nombre de succès de chasse : " , np.sum(result) , " = efficacité %2.f%s"%(100*np.sum(result)/len(result),"%"))





############################################################################
##############################  GRAPHIQUES #################################
############################################################################

if graphiques:

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

    if nombrePredateurs == 1:
        couleurPredateur2 = 'white'
    elif nombrePredateurs == 2:
        couleurPredateur2 = 'b'

    data = np.array([np.vstack((xPos, yPos))])
    data2 = np.array([np.vstack((xPos2, yPos2))])
    data3 = np.array([np.vstack((xPos3, yPos3))])

    # first print the final result
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if crounch:
        state = " la proie est attrapée après %.2f secondes"%(t)
    else:
        state = " la proie s'est enfuie"

    title = 'Trajectoires finales : ' + state +"\n Distance initiale : %.2f m"%(distanceInitiale1)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.set_xlim([min(1.15*min(data[0,0,:]),1.15*min(data2[0,0,:]),1.15*min(data3[0,0,:])),
                 max(1.15*max(data[0,0,:]),1.15*max(data2[0,0,:]),1.15*max(data3[0,0,:]))])
    ax.set_ylim([min(1.15*min(data[0,1,:]),1.15*min(data2[0,1,:]),1.15*min(data3[0,1,:])),
                 max(1.15*max(data[0,1,:]),1.15*max(data2[0,1,:]),1.15*max(data3[0,1,:]))])
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')



    ax.plot(data[0,0,:],data[0,1,:],'r',label="Thescelosaurus (proie)")
    ax.plot(data2[0,0,:],data2[0,1,:],'b',label="Velociraptor (prédateur)")
    ax.plot(data3[0,0,:],data3[0,1,:],color = couleurPredateur2)

    plt.get_current_fig_manager().window.state('zoomed')
    plt.legend()
    plt.show()
    # fig.savefig("./figures/crounch%sstrategie%s2predateursIntelligents.png"%(crounch,strategie), dpi=600)

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

    auv3 = [ax.plot(data3[0][0,0:2], data3[0][1,0:2],   marker=(4,2),color=couleurPredateur2)[0]]
    trj3 = [ax.plot(data3[0][0,0:2], data3[0][1,0:2],color=couleurPredateur2)[0]]


    # Setthe axes properties
    # ,1.15*min(data3[0,0,:]) // ,1.15*max(data3[0,0,:])
    ax.set_xlim([min(1.15*min(data[0,0,:]),1.15*min(data2[0,0,:]),1.15*min(data3[0,0,:])),
                 max(1.15*max(data[0,0,:]),1.15*max(data2[0,0,:]),1.15*max(data3[0,0,:]))])
    ax.set_xlabel('x (m)')

    # ,1.15*min(data3[0,1,:]) // ,1.15*max(data3[0,1,:])
    ax.set_ylim([min(1.15*min(data[0,1,:]),1.15*min(data2[0,1,:]),1.15*min(data3[0,1,:])),
                 max(1.15*max(data[0,1,:]),1.15*max(data2[0,1,:]),1.15*max(data3[0,1,:]))])
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

    ani_auv3 = animation.FuncAnimation(fig, update_auv,frames = frames, fargs=(data3, auv3),
                                       interval=interval, blit=False, repeat=False) #repeat=False,
    ani_trj3 = animation.FuncAnimation(fig, update_trj,frames = frames, fargs=(data3, trj3),
                                       interval=interval, blit=False, repeat=False) #repeat=False,

    plt.get_current_fig_manager().window.state('zoomed')
    plt.legend()
    plt.show()

    # fig = plt.figure()
    # plt.plot(separationVec)
    # plt.show()




