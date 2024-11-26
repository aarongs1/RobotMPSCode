#! /user/bin/python

"""
Example showing how to initialise, configure, and communicate
with NDI Polaris, Vega, and Aurora trackers.
"""

import time
import six
from sksurgerynditracker.nditracker import NDITracker
import RobotControl as rbt
import numpy as np

class Polaris():
    def __init__(self, tracker):
        self.track = False
        self.tracker = tracker
    
    def get_track_status(self):
        return self.track
    
    def set_track_status(self, value):
        self.track = value

tracker = None
track = False

def setup():
    settings_polaris = {"tracker type": "polaris",
    "romfiles" : ['C:/Users/aaron/Desktop/LooLab/Polaris/ToolDefs/PhantomAllPassRotation.rom']}
    tracker = NDITracker(settings_polaris)
    global camera
    camera = Polaris(tracker)


def start(experiment_name, repetitions=None, num_points=None):
    print("Starting Tracking")
    camera.tracker.start_tracking()
    camera.set_track_status(True)
    if experiment_name == 'translation':
        record_translation()
    if experiment_name == 'static position':
        record_position(repetitions, num_points)
    if experiment_name == 'rotation position':
        record_ang_position(repetitions, num_points)
    if experiment_name == 'rotation':
        record_rotation()
    if experiment_name == 'initial position': 
        record_initial_position()
    
def record_initial_position():
    pos_mat = np.empty([1,3])
    for _ in range(20):
        print('bruh')
        frame_info = camera.tracker.get_frame()
        position = frame_info[3][0][:3,3]
        pos_mat = np.vstack([pos_mat, position])
        print(position)
        time.sleep(0.300333)
    stop()
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/initial_position_capture.txt', pos_mat)

def record_translation():
    track = camera.get_track_status()
    pos_mat = np.empty([1,3])

    #get initial position
    frame_info = camera.tracker.get_frame()
    frame_num = frame_info[2][0]
    position = frame_info[3][0][:3,3]
    pos_mat = np.vstack([pos_mat, position])
    
    frame_arr = np.array([])
    while track:
        frame_info = camera.tracker.get_frame()
        frame_num = frame_info[2][0]
        position = frame_info[3][0][:3,3]
        frame_arr = np.append(frame_arr, frame_num)
        pos_mat = np.vstack([pos_mat, position])
        #time.sleep(0.1)
        move_status = rbt.get_move_status()
        print("MOVE_STATUS: ", move_status)
        if move_status:
            camera.set_track_status(False)
            track = camera.get_track_status()
    stop()
    print(pos_mat)
    print(frame_arr)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/translation_pos_mat_50dis_10spd_10reps_1.txt', pos_mat)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/translation_frame_vec_50dis_10spd_10reps_1.txt', frame_arr)

def record_position(repetitions, num_points):
    #stopped = rbt.get_move_status()
    pos_mat = np.empty([1,3])
    frame_arr = np.array([])
    for i in range(repetitions):
        checkpoint = rbt.get_checkpoint()
        print('first: ', checkpoint)
        for j in range(num_points):
            while checkpoint != j+1:
                checkpoint = rbt.get_checkpoint()
                print('loop: ', checkpoint)
                #stopped = rbt.get_move_status()
            print('RECORD_POSITION')
            frame_info = camera.tracker.get_frame()
            frame_num = frame_info[2][0]
            position = frame_info[3][0][:3,3]
            frame_arr = np.append(frame_arr, frame_num)
            pos_mat = np.vstack([pos_mat, position])
            #stopped = False
    stop()
    print(pos_mat)
    print(frame_arr)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/position_pos_mat_5pts_10reps.txt',pos_mat)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/position_frame_vec_5pts_10reps.txt', frame_arr)

def record_ang_position(repetitions, num_points):
    pos_mat = np.empty([1,3])
    frame_arr = np.array([])
    for i in range(repetitions):
        checkpoint = rbt.get_checkpoint()
        print('first: ', checkpoint)
        for j in range(num_points):
            while checkpoint != j+1:
                checkpoint = rbt.get_checkpoint()
                print('loop: ', checkpoint)
            print('RECORD_ANG_POSITION')
            frame_info = camera.tracker.get_frame()
            print(frame_info)
            frame_num = frame_info[2][0]
            position = frame_info[3][0][:3,3]
            frame_arr = np.append(frame_arr, frame_num)
            pos_mat = np.vstack([pos_mat, position])
    stop()
    print(pos_mat)
    print(frame_arr)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/ang_position_pos_mat_10pts_10reps_test.txt', pos_mat)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/ang_position_frame_vec_10pts_10reps_test.txt', frame_arr)

def record_rotation():
    track = camera.get_track_status()
    pos_mat = np.empty([1,3])

    #get initial position
    frame_info = camera.tracker.get_frame()
    frame_num = frame_info[2][0]
    frame_arr = np.array([frame_num])
    position = frame_info[3][0][:3,3]
    pos_mat = np.vstack([pos_mat, position])
    
    while track:
        frame_info = camera.tracker.get_frame()
        frame_num = frame_info[2][0]
        position = frame_info[3][0][:3,3]
        frame_arr = np.append(frame_arr, frame_num)
        pos_mat = np.vstack([pos_mat, position])
        move_status = rbt.get_move_status()
        if move_status:
            camera.set_track_status(False)
            track = camera.get_track_status()
    stop()
    print(pos_mat)
    print(frame_arr)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/rotation_pos_mat_5spd_10reps_13deg.txt', pos_mat)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/rotation_frame_vec_5spd_10reps_13deg.txt', frame_arr)

def record_rotation_fast():
    track = camera.get_track_status()
    x_pos = []
    y_pos = []
    frames = []

    #get initial position
    frame_info = camera.tracker.get_frame()
    frame_num = frame_info[2][0]
    frames.append(frame_num)
    position = frame_info[3][0][:3,3]
    x_pos.append(position[1])
    y_pos.append(position[0])
    
    frame_arr = np.array([])
    while track:
        frame_info = camera.tracker.get_frame()
        frame_num = frame_info[2][0]
        position = frame_info[3][0][:3,3]
        frames.append(frame_num)
        x_pos.append(position[1])
        y_pos.append(position[0])
        move_status = rbt.get_move_status()
        if move_status:
            camera.set_track_status(False)
            track = camera.get_track_status()
    stop()
    print(x_pos)
    print(y_pos)
    print(frame_arr)
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/rotation_xpos_mat_50spd_10reps_13deg.txt', np.array(x_pos))
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/rotation_ypos_mat_50spd_10reps_13deg.txt', np.array(y_pos))
    np.savetxt('C:/Users/aaron/Desktop/LooLab/Meca500_code/RobotMPSCode/PolarisData/rotation_frames_vec_50spd_10reps_13deg.txt', np.array(frames))

def stop():
    print("Stopping tracking")
    camera.tracker.stop_tracking()
    camera.tracker.close()




def run():
    """Demonstration program

    Example showing how to initialise, configure, and communicate
    with NDI Polaris, Vega, and Aurora trackers.
    Configuration is by python dictionaries, edit as necessary.

    Dictionaries for other systems:

    settings_polaris = {"tracker type": "polaris",
    "romfiles" : ["../data/8700339.rom"]}

    settings_aurora = {
        "tracker type": "aurora",
        "ports to probe": 2,
        "verbose": True,
    }

    settings_dummy = {"tracker type": "dummy",}

    """

    settings_polaris = {"tracker type": "polaris",
    "romfiles" : ['C:/Users/aaron/Desktop/LooLab/Polaris/ToolDefs/PhantomFlatUniqueSegPass2.rom']}
    tracker = NDITracker(settings_polaris)

    tracker.start_tracking()

    #six.print_(tracker.get_tool_descriptions())
    for _ in range(20):
        print('bruh')
        six.print_(tracker.get_frame())
        time.sleep(0.300333)

    tracker.stop_tracking()
    tracker.close()

if __name__ == "__main__":
    run()