from sympy import *
from sympy.geometry import *
from sympy.plotting import plot
import numpy as np
import math

from Dinosaure import Dinosaure

import matplotlib.pyplot as plt
import matplotlib.animation as animation

dinosaure1 = Dinosaure(5,10,np.array([0,0]))
dinosaure1.direction = np.array([0,1])

dinosaure2 = Dinosaure(10,15,np.array([30,0]))
dinosaure2.direction = np.array([0,-1])

print(dinosaure1)

xPos = [dinosaure1.getX()]
yPos = [dinosaure1.getY()]
xPos2 = [dinosaure2.getX()]
yPos2 = [dinosaure2.getY()]

angle = []

tmax = 150
t = 0
dt = 0.25
destination = np.array([-300,-1])
while (t<tmax):
    print("---")
    t += dt
    if np.linalg.norm(np.subtract(dinosaure1.position,dinosaure2.position)) <= 5:
        destination = dinosaure1.position + 1000* np.array([-dinosaure1.direction[1],dinosaure1.direction[0]])

    dinosaure1.seDeplacer(destination,dt)
    dinosaure2.seDeplacer(dinosaure1.position,dt)

    xPos.append(dinosaure1.getX())
    yPos.append(dinosaure1.getY())
    xPos2.append(dinosaure2.getX())
    yPos2.append(dinosaure2.getY())


############################################################################
##############################  GRAPHIQUES #################################
############################################################################

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

n=int(np.round(tmax/dt))
# Create line objects:
auv = [ax.plot(data[0][0,0:2], data[0][1,0:2],  'ro')[0]]
trj = [ax.plot(data[0][0,0:2], data[0][1,0:2],':r')[0]]

auv2 = [ax.plot(data2[0][0,0:2], data2[0][1,0:2],   marker=(5, 2),color='b')[0]]
trj2 = [ax.plot(data2[0][0,0:2], data2[0][1,0:2],':b')[0]]

# ax.plot(0,300,'xr')
# ax.plot(destination[0],destination[1],'xr')

# Setthe axes properties
ax.set_xlim([min(1.15*min(data[0,0,:]),1.15*min(data2[0,0,:])), max(1.15*max(data[0,0,:]),1.15*max(data2[0,0,:]))])
ax.set_xlabel('X')

ax.set_ylim([min(1.15*min(data[0,1,:]),1.15*min(data2[0,1,:])), max(1.15*max(data[0,1,:]),1.15*max(data2[0,1,:]))])
ax.set_ylabel('Y')

# ax.set_zlim3d([-1.0, 1.0])
# ax.set_zlabel('Z')

ax.set_title('2D Test')

# Creating the Animation object
ani_auv = animation.FuncAnimation(fig, update_auv, n, fargs=(data, auv),
                                  interval=50, blit=False, repeat=False) #repeat=False,
ani_trj = animation.FuncAnimation(fig, update_trj, n, fargs=(data, trj),
                                  interval=50, blit=False, repeat=False) #repeat=False,

ani_auv2 = animation.FuncAnimation(fig, update_auv, n, fargs=(data2, auv2),
                                  interval=50, blit=False, repeat=False) #repeat=False,
ani_trj2 = animation.FuncAnimation(fig, update_trj, n, fargs=(data2, trj2),
                                  interval=50, blit=False, repeat=False) #repeat=False,

plt.show()

#
# fig = plt.figure()
# plt.plot(angle)
# plt.show()
