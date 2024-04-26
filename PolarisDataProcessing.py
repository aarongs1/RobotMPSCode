import os
import numpy as np
import matplotlib.pyplot as plt

pos_mat = np.loadtxt('RobotMPSCode/PolarisData/pos_mat10_50dist_10speed.txt')
frame_arr = np.loadtxt('RobotMPSCode/PolarisData/frame_vec10_50dist_10speed.txt')

pos_mat = pos_mat[2:,:]
frame_arr = frame_arr[1:]
frame_arr = frame_arr - frame_arr[0]

freq = 60 #freq at which frame number is increased
T = 1/freq  #period between 1 frame

frame_arr = frame_arr*T   #multiply frames by period of each frame to get timestamps in seconds

x = pos_mat[:,0]
y = pos_mat[:,1]
z = pos_mat[:,2]
 
plt.plot(frame_arr, x, 'o')
# plt.plot(frame_arr, y, 'o')
# plt.plot(frame_arr, z, 'o')

plt.show()