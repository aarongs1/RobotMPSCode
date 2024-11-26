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

def ang_position():
    path = 'RobotMPSCode/PolarisData'
    pos_list = glob.glob(path + '/ang_position_pos*')
    num_pts = 10
 
    for pos_path in pos_list:
        pos_mat = np.loadtxt(pos_path)
        pos_mat = pos_mat[1:,:]


        for i in range(num_pts):
            point_list = pos_mat[i::num_pts,:]
            x_std, y_std, z_std = np.std(point_list[:,0]), np.std(point_list[:,1]), np.std(point_list[:,2])
            print('Point ' + str(i+1) + ' std: ', x_std, y_std, z_std)

        y = pos_mat[:,0]
        x = pos_mat[:,1]
        z = pos_mat[:,2]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.view_init(azim=-30, elev=-160)

        ax.scatter(z, y, x, marker='o')

        ax.set_xlabel('X Pos (mm)')
        ax.set_ylabel('Y Pos (mm)')
        ax.set_zlabel('Z Pos (mm)')

        ax.axes.set_ylim3d(bottom=-60, top=60)
        ax.set_xlim(-1500, -1300) 

        plot_filename = ''.join(pos_path.split('mat_')[1].split('.txt')[0])

        plt.title(plot_filename)

        plt.savefig(path + '/' + plot_filename + '.png')
     
        plt.close()

        plt.show()

def rotation():
    #error = 0.018 - 0.025
    freq = 60 #freq at which frame number is increased
    T = 1/freq  #period between 1 frame

    gear_ratio = 2.5
    #ang_speed_per = 15 #percent
    #ang_speed = (ang_speed_per/100)*500*gear_ratio #deg/s
    max_angle = 13*gear_ratio

    # T_des = max_angle*4/ang_speed
    # f_des = 1/T_des
 
    # x_0 = -161.04 #mm
    # y_0 = 180.03 #mm
    #x_0 = -161.28 #mm
    #y_0 = 180.32 #mm
    L = 103 #mm

    path = 'RobotMPSCode/PolarisData'
    dir_list = os.listdir(path)
    frame_list = glob.glob(path + '/rotation_frame_vec_5spd_10reps_13deg*')
    pos_list = glob.glob(path + '/rotation_pos_mat_5spd_10reps_13deg*')

    for frame_path, pos_path in zip(frame_list, pos_list):

        plot_filename = ''.join(pos_path.split('mat')[1].split('.txt')[0])
        ang_speed_per = int(plot_filename.split('_')[1].split('spd')[0])   #percent
        ang_speed = (ang_speed_per/100)*500*gear_ratio #deg/s
        T_des = max_angle*4/ang_speed
        f_des = 1/T_des

        frame_arr = np.loadtxt(frame_path)
        pos_mat = np.loadtxt(pos_path)

        n = 41
        # x_0 = np.mean(pos_mat[1:n,1])
        # y_0 = np.mean(pos_mat[1:n,0])
        pos_mat = pos_mat[n:,:]
        frame_arr = frame_arr - frame_arr[n-1]

        time_arr = frame_arr*T   #multiply frames by period of each frame to get timestamps in seconds
        time_arr = time_arr[n-1:]
        y = pos_mat[:,0]
        x = pos_mat[:,1]
        z = pos_mat[:,2]
        
        fig, (ax1, ax2) = plt.subplots(2)
        if ang_speed_per == 5:
            # x_0 = -145.52 #x[0]
            # y_0 = 155.88 #y[0]
            x_0 = -146.94#x[0]
            y_0 = 156.18 #y[0]
        elif ang_speed_per == 15:
            x_0 = -146.39
            y_0 = 155.91
        
        t = np.linspace(time_arr[0], time_arr[-1], 500)
        theta_des = max_angle*signal.sawtooth(2*np.pi*f_des*t, 0.5)   #deg
        x_des = L*(np.sin(max_angle*np.pi/180) + np.sin(theta_des*np.pi/180)) + x_0 #mm
        y_des = -L*(np.cos(theta_des*np.pi/180) - np.cos(max_angle*np.pi/180)) + y_0  #mm

        theta_pred = max_angle*signal.sawtooth(2*np.pi*f_des*time_arr, 0.5) #deg
        # theta_diff = theta_pred[0] - theta_d[0]
        # print(theta_diff)
        # theta_pred = theta_pred + theta_diff
        x_pred = L*(np.sin(max_angle*np.pi/180) + np.sin(theta_pred*np.pi/180)) + x_0 #mm
        y_pred = -L*(np.cos(theta_pred*np.pi/180) - np.cos(max_angle*np.pi/180)) + y_0  #mm

        ax1.plot(t, x_des, color='m', label='Desired Trajectory (x)')
        ax2.plot(t, y_des, color='y', label='Desired Trajectory (y)')
        #plt.plot(t, theta_des, color='r', label='Desired Angle')
        ax1.plot(time_arr, x, 'o', markersize=3, color='b', label='Tracked Position (x)')
        ax2.plot(time_arr, y, 'o', markersize=3, color='g', label='Tracked Position (y)')
        # ax1.plot(time_arr, x_pred, 'o', markersize=3, color='k', label='Predicted Position (x)')
        # ax2.plot(time_arr, y_pred, 'o', markersize=3, color='r', label='Predicted Position (y)')
        #plt.plot(time_arr, z, 'o', markersize=3, color='r', label='Tracked Position (z)')     
 
        plot_filename = ''.join(pos_path.split('mat')[1].split('.txt')[0])
        fig.supxlabel('Time (s)')
        # fig.supylabel('Position (mm)')
        ax1.set_ylabel('X Position (mm)')
        ax2.set_ylabel('Y Position (mm)')
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)
        ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)
         
        plt.subplots_adjust(wspace=0.5, hspace=0.3)
        
        RMS_Error_x = np.sqrt(np.mean((x - x_pred)**2))
        mean_diff_x = np.mean(np.abs(x - x_pred))
        RMS_Error_y = np.sqrt(np.mean((y - y_pred)**2))
        mean_diff_y = np.mean(np.abs(y - y_pred))
        print("X Mean difference " + str(ang_speed_per) + ": ", mean_diff_x)
        print("X RMS difference " + str(ang_speed_per) + ": ", RMS_Error_x)
        print("Y Mean difference " + str(ang_speed_per) + ": ", mean_diff_y)
        print("Y RMS difference " + str(ang_speed_per) + ": ", RMS_Error_y) 
        # plt.text(0, -1270, 'RMS Error: ' + str(RMS_Error))
        # plt.title(plot_filename + ', ' + 'RMS Error: ' + str(round(RMS_Error, 3)))

        # fig.suptitle(plot_filename + '_Rotation')

        fig.savefig(path + '/' + plot_filename + '.png')

        # fig.close()

def rotation_fast():
    #error = 0.018 - 0.025
    freq = 60 #freq at which frame number is increased
    T = 1/freq  #period between 1 frame

    gear_ratio = 2.5
    #ang_speed_per = 15 #percent
    #ang_speed = (ang_speed_per/100)*500*gear_ratio #deg/s
    max_angle = 13*gear_ratio

    # T_des = max_angle*4/ang_speed
    # f_des = 1/T_des
 
    # x_0 = -161.04 #mm
    # y_0 = 180.03 #mm
    #x_0 = -161.28 #mm
    #y_0 = 180.32 #mm
    L = 103 - 100 #mm

    path = 'RobotMPSCode/PolarisData'
    dir_list = os.listdir(path)
    frame_list = glob.glob(path + '/rotation_frames_vec*')
    xpos_list = glob.glob(path + '/rotation_xpos_mat*')
    ypos_list = glob.glob(path + '/rotation_ypos_mat*')

    for frame_path, xpos_path, ypos_path in zip(frame_list, xpos_list, ypos_list):

        plot_filename = ''.join(xpos_path.split('mat')[1].split('.txt')[0])
        ang_speed_per = int(plot_filename.split('_')[1].split('spd')[0])   #percent
        ang_speed = (ang_speed_per/100)*500*gear_ratio #deg/s
        T_des = max_angle*4/ang_speed
        f_des = 1/T_des

        frame_arr = np.loadtxt(frame_path)
        xpos = np.loadtxt(xpos_path)
        ypos = np.loadtxt(ypos_path)


        # pos_mat = pos_mat[2:,:]
        frame_arr = frame_arr - frame_arr[0]

        time_arr = frame_arr*T   #multiply frames by period of each frame to get timestamps in seconds

        
        fig, (ax1, ax2) = plt.subplots(2)
        if ang_speed_per == 5:
            x_0 = -145.52 #x[0]
            y_0 = 155.88 #y[0]
        elif ang_speed_per == 15:
            x_0 = -146.39
            y_0 = 155.91
         
        t = np.linspace(0, time_arr[-1], 500)
        theta_des = max_angle*signal.sawtooth(2*np.pi*f_des*t, 0.5)   #deg
        x_des = L*(np.sin(max_angle*np.pi/180) + np.sin(theta_des*np.pi/180)) + x_0 #mm
        y_des = -L*(np.cos(theta_des*np.pi/180) - np.cos(max_angle*np.pi/180)) + y_0  #mm
        ax1.plot(t, x_des, color='m', label='Desired Trajectory (x)')
        ax2.plot(t, y_des, color='y', label='Desired Trajectory (y)')
        #plt.plot(t, theta_des, color='r', label='Desired Angle')
        ax1.plot(time_arr, xpos, 'o', markersize=3, color='b', label='Tracked Position (x)')
        ax2.plot(time_arr, ypos, 'o', markersize=3, color='g', label='Tracked Position (y)')
        #plt.plot(time_arr, z, 'o', markersize=3, color='r', label='Tracked Position (z)')     
 
        plot_filename = ''.join(xpos_path.split('mat')[1].split('.txt')[0])
        fig.supxlabel('Time (s)')
        fig.supylabel('Position (mm)')

        ax1.legend(loc='upper right')
        ax2.legend(loc='upper right')
         

        # pos_pred = start_z + distance/2 + (distance/2)*signal.sawtooth(2*np.pi*f_des*time_arr, 0.5)
        # RMS_Error = np.sqrt(np.mean((z - pos_pred)**2))
        # mean_diff = np.mean(np.abs(z - pos_pred))
        # print("Mean difference: ", mean_diff)
        # print("RMS difference: ", RMS_Error)
        # plt.text(0, -1270, 'RMS Error: ' + str(RMS_Error))
        # plt.title(plot_filename + ', ' + 'RMS Error: ' + str(round(RMS_Error, 3)))

        fig.suptitle(plot_filename + '_Rotation')

        fig.savefig(path + '/' + plot_filename + '_fast' + '.png')

        # fig.close()


if __name__ == "__main__":
    ang_position()