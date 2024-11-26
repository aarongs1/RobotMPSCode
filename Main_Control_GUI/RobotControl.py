import mecademicpy.robot as mdr
import mecademicpy.mx_robot_def as mx_robot
import serial
import time
import numpy as np
import PolarisTracking as polaris

'''''''''''''''
Class that keeps track of the status of the robot including initialization status, 
mouse status (whether it has picked up a mouse or not), and beam position status (whether the robot is close to beam)
'''''''''''''''
class Status():
    def __init__(self):
        self.initialize = False
        self.mouse_present = False
        self.beam_pos = False

    def set_initialize(self):
        self.initialize = True
    
    def get_initialize(self):
        return self.initialize
    
    def set_mouse_status(self):
        self.mouse_present = True

    def get_mouse_status(self):
        return self.mouse_present
    
    def get_beam_pos_status(self):
        return self.beam_pos
    
    def set_beam_pos_status(self, value):
        self.beam_pos = value

def default():   
    pass 

'''''''''''''''
Resets error status from robot arm
'''''''''''''''
def reset_error():
    robot.ResetError()
    robot.ClearMotion()
    robot.ResumeMotion()

'''''''''''''''
Initializes robot arm with IP address
'''''''''''''''
def initialize_robot(): 
    global robot
    robot = mdr.Robot()                     #connect to robot's ip address
    robot.Connect(address='192.168.0.100')
    robot.ActivateRobot()                   #activate and home robot
    robot.Home()
    robot.WaitHomed()
    robot.SetRealTimeMonitoring('all')      #to be able to monitor joint pos, vel, etc.
    global robotStatus
    robotStatus = Status()
    robotStatus.set_initialize()

'''''''''''''''
Function for rest position command. If you wish to change the rest position, change the coordinates
in the robot.MovePose command that has the following format (x,y,z,euler angle 1,euler angle 2,euler angle 3)
'''''''''''''''
def rest_pos():
    if robotStatus.get_initialize():
        if robotStatus.get_beam_pos_status():
            robotStatus.set_beam_pos_status(False)
            clear_beam() 
        robot.SetJointVel(10)
        robot.SetConf(1,1,-1)
        robot.MovePose(155,0,170,0,90,0)
    else:
        raise Exception("Robot not activated and homed")

'''''''''''''''
Function for approaching and positioning the mouse close to beam. The robot will move to position with z=350 and then slowly move 
in a straight line vertically up to z=395. These values were for the Mobetron but might need to be changed/calibrated for different systems or may not
according to where/on what the robot is mounted
'''''''''''''''
def beam_pos():
    if robotStatus.get_initialize():
        robotStatus.set_beam_pos_status(True)
        robot.SetJointVel(10)
        robot.SetConf(1,1,1)
        robot.MovePose(70,0,350,0,90,0)
        robot.SetCartLinVel(5)
        robot.MoveLin(70,0,395,0,90,0)
    else:
        raise Exception("Robot not activated and homed")
    
'''''''''''''''
Function used for testing the pickup position of the mouse (origin position). 
'''''''''''''''
def origin_pos():
    if robotStatus.get_initialize():
        robot.SetCartLinVel(5)
        robot.SetJointVel(10)
        robot.SetConf(1,1,-1)
        robot.MovePose(158,0,130,0,90,0)
        robot.MoveLin(158,0,110.5,0,90,0)
        robot.MoveLin(155.5,0,110.5,0,90,0)
    else:
        raise Exception("Robot not activated and homed")

'''''''''''''''
Outer function used by GUI to pick up mouse holder, pick up position defined by x,y,z
For the function that carries out the actual commands to pick up the mouse see "pickup" function
'''''''''''''''
def pickup_mouse():
    x = 155
    y = 0
    z = 110.5
    joint_vel = 10
    cart_vel = 10
    if robotStatus.get_initialize():
        if robotStatus.get_beam_pos_status():
            robotStatus.set_beam_pos_status(False)
            clear_beam()
        pickup(0, 0, (x,y,z), joint_vel, cart_vel, initial_placement=True)
        robotStatus.set_mouse_status()
    else:
        raise Exception("Robot not activated and homed")

'''''''''''''''
Function that GUI references to offset mouse holder rotation axis by specified amount horizontally and vertically
Inputs: hor_offset (mm), vert_offset (mm)
'''''''''''''''
def offset_axis(hor_offset, vert_offset):
    x = 155
    y = 0
    z = 110
    joint_vel = 10
    cart_vel = 10
    if not robotStatus.get_mouse_status():
        raise Exception("Mouse not present")
    elif not robotStatus.get_initialize():
        raise Exception("Robot not activated and homed") 
    else:
        pickup(hor_offset, vert_offset, (x,y,z), joint_vel, cart_vel)

'''''''''''''''
Function used by GUI to rotate mouse to a certain angle and back with certain angular speed and for x repetitions
Inputs: angle (degrees), ang_vel (% of max end effector speed), repetitions
'''''''''''''''
def rotate_mouse(angle, ang_vel, repetitions):
    if robotStatus.get_initialize():
        rotation(angle, ang_vel, repetitions)
    else:
        raise Exception("Robot not activated and homed")
    
'''''''''''''''
Function used by GUI to translate mouse (parallel to floor) by a certain distance and back at desired linear speed and for x repetitions
Inputs: lin_vel (mm/s), repetitions, distance (mm)
'''''''''''''''    
def translate_mouse(lin_vel, repetitions, distance):
    if robotStatus.get_initialize():
        translation(distance, repetitions, lin_vel)
    else:
        raise Exception("Robot not activated and homed")

'''''''''''''''
Function used by GUI to translate robot linearly in x,y,z
'''''''''''''''  
def jog_robot(direction, speed):
    if robotStatus.get_initialize():
        if direction == "Z_pos":
            robot.MoveLinVelWrf(0,0,speed,0,0,0)
        if direction == "Z_neg":
            robot.MoveLinVelWrf(0,0,-speed,0,0,0)
        if direction == "Y_pos":
            robot.MoveLinVelWrf(0,speed,0,0,0,0)
        if direction == "Y_neg":
            robot.MoveLinVelWrf(0,-speed,0,0,0,0)
        if direction == "X_pos":
            robot.MoveLinVelWrf(speed,0,0,0,0,0)
        if direction == "X_neg":
            robot.MoveLinVelWrf(-speed,0,0,0,0,0)
    else:
        raise Exception("Robot not activated and homed")

#####################################################################################
    
'''''''''''''''
The following functions are all used for performing movements for experiments with the Polaris Spectra tracking system
These are not useful for general robot movement, unless you would like to use these for doing work the Polaris
'''''''''''''''  
def position_experiment(num_points):
    if robotStatus.get_initialize():
        repetitions = 10
        angle_range = 28.78 - 5.59
        r = 740.74
        points = [(158,110.5)]
        if num_points:
             interval = angle_range/(num_points-1)
             for i in range(num_points-1):
                 angle_rad = (5.59 + (i+1)*interval)*np.pi/180
                 points.append((r*np.cos(angle_rad) - 579.22, 38.33 + r*np.sin(angle_rad)))
        points.append((70,395)) 
        robot.SetJointVel(10)
        robot.SetCartLinVel(10)
        for i in range(repetitions):
            robot.SetConf(1,1,-1)
            first_point = points[0]
            robot.MovePose(first_point[0],0,first_point[1]+20,0,90,0)
            robot.MoveLin(first_point[0],0,first_point[1],0,90,0)
            robot.Delay(1)
            robot.SetCheckpoint(1)
            robot.Delay(2)
            checkpoint_num = 2
            for point in points[1:]: 
                if point[1] > 300:
                    robot.SetConf(1,1,1)
                robot.MovePose(point[0],0,point[1],0,90,0)
                robot.Delay(1)
                robot.SetCheckpoint(checkpoint_num)
                robot.Delay(2) 
                checkpoint_num += 1
        polaris.start('static position', repetitions, num_points)
    else:
        raise Exception("Robot not activated and homed")
    
def polaris_setup():
    polaris.setup()

def polaris_position():
    polaris.start('initial position')

def translation_experiment(repetitions):
    if robotStatus.get_initialize():
        translation(50, repetitions, 10)
        polaris.start('translation')
        #robot.SetCheckpoint(1)
    else:
        raise Exception("Robot not activated and homed")
    
def rot_position_experiment(num_points):
    if robotStatus.get_initialize():
        repetitions = 10
        angle_range = 26
        points = [-13]
        if num_points:
             interval = angle_range/(num_points-1)
             for i in range(num_points-1):
                 angle = -13 + (i+1)*interval
                 points.append(angle)
        robot.SetJointVel(10)
        robot.SetCartLinVel(10)
        checkpoint_num = 1
        for i in range(repetitions):
            checkpoint_num = 1
            for point in points: 
                robot.MovePose(155,0,170,point,90,0)
                robot.Delay(1)
                robot.SetCheckpoint(checkpoint_num)
                robot.Delay(2) 
                checkpoint_num += 1
        polaris.start('rotation position', repetitions, num_points)
    else:
        raise Exception("Robot not activated and homed")

def rotation_experiment(repetitions):
    if robotStatus.get_initialize():
        angle = 13
        angle_vel_per = 5
        robot.SetJointVel(10)
        robot.MovePose(155,0,170,-angle,90,0)
        robot.Delay(1)
        for i in range(repetitions):
            rotation_arc(angle, angle_vel_per)
        polaris.start('rotation')
    else:
        raise Exception("Robot not activated and homed")
    
def helix_experiment(repetitions):
    if robotStatus.get_initialize():
        for i in range(repetitions):
            print("helix")
            time.sleep(1)
            helix(20, 10, 210, 50)
    else:
        raise Exception("Robot not activated and homed")


################################################################

"""""""""""""""
Main functions defining general robot movements
"""""""""""""""

"""""""""""""""
Function for offsetting rotation axis of mouse holder
Inputs: hor_offset (mm), vert_offset (mm), pickup_pos (x,y,z) in mm, joint_vel (% of max speed), cart_vel (mm/s)
"""""""""""""""
def pickup(hor_offset, vert_offset, pickup_pos, joint_vel, cart_vel, initial_placement=False):
    robot.SetConf(1,1,-1)
    x, y, z = pickup_pos

    #move down
    if y > 0:
        #if offseting axis
        robot.SetJointVel(joint_vel)
        robot.MovePose(x+4,y,z+70,0,90,0)
        robot.SetCartLinVel(cart_vel)
        robot.MoveLin(x+4,y,z+10,0,90,0)
        robot.SetCartLinVel(int(cart_vel/2))
        robot.MoveLin(x+4,y,z,0,90,0)
        robot.Delay(1)
    else:  
        #if picking up mouse 
        robot.SetJointVel(joint_vel)
        robot.MovePose(x+6,y,z+70,0,90,0)
        robot.SetCartLinVel(cart_vel)
        robot.MoveLin(x+6,y,z+10,0,90,0)
        robot.SetCartLinVel(int(cart_vel/2))
        robot.MoveLin(x+6,y,z,0,90,0)
        robot.Delay(1)

    #push spring wall back
    robot.MoveLin(x+3,y,z,0,90,0)
    robot.Delay(1)
    robot.MoveLin(x-0.5,y,z,0,90,0)

    if initial_placement:
        robot.Delay(10)
    else:
        robot.Delay(2)

    #offset axis
    robot.MoveLin(x,hor_offset,z+vert_offset,0,90,0)
    robot.MoveLin(x+3,hor_offset,z+vert_offset,0,90,0)

    #move back up
    robot.MoveLin(x+3,hor_offset,z+30,0,90,0) 
    robot.SetJointVel(joint_vel)
    robot.MovePose(x+6,0,z+70,0,90,0)

'''''''''''''''
Function to rotate mouse to a certain angle and back with certain angular speed and for x repetitions
Inputs: angle (degrees), ang_vel (% of max end effector speed), repetitions
'''''''''''''''
def rotation(angle, ang_vel, repetitions):
    robot.WaitIdle()
    robot_data = robot.GetRobotRtData()
    curr_joint_pos = robot_data.rt_joint_pos.data
    #print(curr_joint_pos)
    # robot.SetJointVel(int(ang_vel/2))
    # robot.MoveJoints(*curr_joint_pos[:5],int(angle/6))
    #ser.write("R\n".encode('utf-8'))
    robot.SetJointVel(ang_vel)
    for _ in range(repetitions):
        robot.MoveJoints(*curr_joint_pos[:5],angle)
        robot.MoveJoints(*curr_joint_pos[:5],0)
    robot.SetJointVel(int(ang_vel/2))

'''''''''''''''
Function to rotate mouse clockwise and counterclockwise within an arc bounded by -angle and angle
Inputs: angle (degrees), ang_vel (% of max end effector speed)
'''''''''''''''
def rotation_arc(angle, ang_vel):
    robot.SetJointVel(ang_vel)
    robot.MovePose(155,0,170,angle,90,0)
    robot.MovePose(155,0,170,-angle,90,0)

'''''''''''''''
Function to translate mouse (parallel to floor) by a certain distance and back at desired linear speed and for x repetitions
Inputs: distance (mm), iterations, lin_vel (mm/s) 
''''''''''''''' 
def translation(distance, iterations, lin_vel):
    #robot.WaitIdle()
    robot.SetCartLinVel(lin_vel)
    for _ in range(iterations):
        robot.MoveLinRelTRF(0,0,distance,0,0,0)
        robot.MoveLinRelTRF(0,0,-distance,0,0,0)

'''''''''''''''
Function to translate mouse (parallel to floor) by a certain distance and back at desired linear speed while simultaneously
rotating mouse by certain angle at desired angular speed
Inputs: distance (mm), lin_vel (mm/s), angle (degrees), angular velocity (% of max joint speed)
''''''''''''''' 
def helix(distance, lin_vel, angle, ang_vel):
    robot.WaitIdle()
    robot.SetCartLinVel(lin_vel)
    robot.SetJointVel(ang_vel)
    robot.MoveLinRelTRF(0,0,distance,0,0,angle)
    robot.MoveLinRelTRF(0,0,-distance,0,0,-angle)

'''''''''''''''
Function to clear robot from beam area defined by beam position command
''''''''''''''' 
def clear_beam():
    robot.SetCartLinVel(5)
    robot.SetConf(1,1,1)
    robot.MoveLin(70,0,350,0,90,0)

def waitTrigger(msg, data, ser):
    while data != msg:
        data = ser.readline().decode().strip()
    data = 0

'''''''''''''''
Function to check if robot is moving
''''''''''''''' 
def get_move_status():
    robot_status = robot.GetStatusRobot()
    return robot_status.end_of_block_status

'''''''''''''''
Function to get current checkpoint of movement command
''''''''''''''' 
def get_checkpoint():
    robot_data = robot.GetRobotRtData()  
    return robot_data.rt_checkpoint.data[0]

#Everything below this is only run if you run this python script itself
if __name__ == "__main__":
    program = 1

    #setup serial
    comport = 'COM7'
    baudrate = 115200
    ser = serial.Serial(comport, baudrate, timeout=0.1)
    data = 0
    time = ''
    msg = 'TRIGGER'

    #solely for positioning mouse relative to beam
    if program == 1:
        robot.SetConf(1,1,1)
        x = 155
        y = 0
        z = 110
        joint_vel = 10
        cart_vel = 10
        robot.MoveLin(70,0,350,0,90,0)
        robot.SetConf(1,1,-1)
        pickup(0, (x,y,z), joint_vel, cart_vel, initial_placement=True)
        robot.SetConf(1,1,1)
        robot.MovePose(70,0,350,0,90,0)
        robot.SetJointVel(5)
        robot.MoveLin(70,0,395,0,90,0)
        rotation(360, 100)


    #testing rotation and multiple pickups
    elif program == 2:
        prev_offset = 0
        x = 155
        y = 0
        z = 110
        joint_vel = 10
        cart_vel = 10
        curr_offset = 10
        rotation_angle = 360
        rotation_vel = 100
        #mx_robot.MX_ST_RT_JOINT_POS
        robot.SetRealTimeMonitoring('all')
        pickup(curr_offset, (x,y,z), joint_vel, cart_vel, initial_placement=True)
        robot.Delay(2)
        #wait for trigger from Arduino
        waitTrigger(msg, data, ser)
        rotation(rotation_angle, rotation_vel)
        time = ser.readline().decode()
        print("TIME: ", time)
        robot.Delay(2)
        prev_offset = curr_offset
        curr_offset = 0
        pickup(curr_offset, (x,prev_offset,z), joint_vel, cart_vel)
        robot.Delay(2)
        #wait for trigger from Arduino
        waitTrigger(msg, data, ser)
        rotation(rotation_angle, rotation_vel)
        time = ser.readline().decode()
        print("TIME: ", time)
        time = ''
    robot.WaitIdle()


