import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
 

def translation():
    #error = 0.018 - 0.025
    start_z = -1314.5

    freq = 60 #freq at which frame number is increased
    T = 1/freq  #period between 1 frame

    speed = 10 #mm/s
    distance = 50 #mm
    T_des = (2*distance)/speed
    f_des = 1/T_des

    path = 'RobotMPSCode/PolarisData'
    dir_list = os.listdir(path)
    frame_list = glob.glob(path + '/frame_vec*')
    pos_list = glob.glob(path + '/pos_mat*')

    for frame_path, pos_path in zip(frame_list, pos_list):

        frame_arr = np.loadtxt(frame_path)
        pos_mat = np.loadtxt(pos_path)


        pos_mat = pos_mat[1:,:]
        frame_arr = frame_arr - frame_arr[0]

        time_arr = frame_arr*T   #multiply frames by period of each frame to get timestamps in seconds

        x = pos_mat[:,0]
        y = pos_mat[:,1]
        z = pos_mat[:,2]
        
        t = np.linspace(0, time_arr[-1], 500)
        pos_des = start_z + distance/2 + (distance/2)*signal.sawtooth(2*np.pi*f_des*t, 0.5)
        plt.plot(t, pos_des, color='b', label='Desired Trajectory')
        plt.plot(time_arr, z, 'o', markersize=3, color='r', label='Tracked Position')     

        plot_filename = ''.join(pos_path.split('mat')[1].split('.txt')[0])

        plt.xlabel('Time (s)')
        plt.ylabel('Position (mm)')

        plt.legend(loc='upper right')
        plt.ylim(-1315, -1255)

        pos_pred = start_z + distance/2 + (distance/2)*signal.sawtooth(2*np.pi*f_des*time_arr, 0.5)
        RMS_Error = np.sqrt(np.mean((z - pos_pred)**2))
        mean_diff = np.mean(np.abs(z - pos_pred))
        print("Mean difference: ", mean_diff)
        print("RMS difference: ", RMS_Error)
        # plt.text(0, -1270, 'RMS Error: ' + str(RMS_Error))
        plt.title(plot_filename + ', ' + 'RMS Error: ' + str(round(RMS_Error, 3)))

        plt.savefig(path + '/' + plot_filename + '.png')

        plt.close()

def position():
    path = 'RobotMPSCode/PolarisData'
    pos_list = glob.glob(path + '/position_pos*')
    num_pts = 5

    for pos_path in pos_list:
        pos_mat = np.loadtxt(pos_path)
        pos_mat = pos_mat[1:,:]


        for i in range(num_pts):
            point_list = pos_mat[i::5,:]
            x_std, y_std, z_std = np.std(point_list[:,0]), np.std(point_list[:,1]), np.std(point_list[:,2])
            #print('Point ' + str(i+1) + ' std: ', x_std, y_std, z_std)

        x = pos_mat[:,0]
        y = pos_mat[:,1]
        z = pos_mat[:,2]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.view_init(azim=-44, elev=-151)

        ax.scatter(z, y, x, marker='o')

        ax.set_xlabel('X Pos (mm)')
        ax.set_ylabel('Y Pos (mm)')
        ax.set_zlabel('Z Pos (mm)')

        ax.axes.set_ylim3d(bottom=-140, top=0) 

        plot_filename = ''.join(pos_path.split('mat_')[1].split('.txt')[0])

        plt.title(plot_filename)

        plt.savefig(path + '/' + plot_filename + '.png')
    
        plt.close()

if __name__ == "__main__":
    translation()