import mecademicpy.robot as mdr
import mecademicpy.mx_robot_def as mx_robot
import serial
import time
import numpy as np
import PolarisTracking as polaris

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

"""""""""""""""
Functions for LabVIEW
"""""""""""""""
def nothing(a=1,b=2):
    return 0

def multiply(factor):
    factor_int = int(factor)
    print(factor_int*10)

def add(num):
    num_int = int(num)
    print(num_int + 5)

#define global variables for labview


def default():   
    pass 

def reset_error():
    robot.ResetError()
    robot.ClearMotion()
    robot.ResumeMotion()

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
        pickup(0, (x,y,z), joint_vel, cart_vel, initial_placement=True)
        robotStatus.set_mouse_status()
    else:
        raise Exception("Robot not activated and homed")

def offset_axis(hor_offset):
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
        pickup(hor_offset, (x,y,z), joint_vel, cart_vel)

def rotate_mouse(ang_vel):
    if robotStatus.get_initialize():
        rotation(360, ang_vel)
    else:
        raise Exception("Robot not activated and homed")
    
def translate_mouse(lin_vel):
    if robotStatus.get_initialize():
        translation(20, lin_vel)
    else:
        raise Exception("Robot not activated and homed")
    
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
    print('Not Implemented')

def translation_experiment(repetitions):
    if robotStatus.get_initialize():
        for i in range(repetitions):
            translation(50, 10)
        polaris.start('translation')
        #robot.SetCheckpoint(1)
    else:
        raise Exception("Robot not activated and homed")
    
def rot_position_experiment(num_points):
    if robotStatus.get_initialize():
        repetitions = 10
        angle_range = 26
        points = [(-13)]
        if num_points:
             interval = angle_range/(num_points-1)
             for i in range(num_points-1):
                 angle = -30 + (i+1)*interval
                 points.append(angle)
        points.append(13) 
        robot.SetJointVel(10)
        robot.SetCartLinVel(10)
        for i in range(repetitions):
            for point in points: 
                robot.MovePose(161,0,180.5,point[i],90,0)
                robot.Delay(1)
                robot.SetCheckpoint(checkpoint_num)
                robot.Delay(2) 
                checkpoint_num += 1
        polaris.start('rotation position', repetitions, num_points)
    else:
        raise Exception("Robot not activated and homed")

def rotation_experiment(repetitions):
    if robotStatus.get_initialize():
        for i in range(repetitions):
            print("rotation")
            time.sleep(1)
            rotation(360, 100)
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


"""""""""""""""
Main functions defining general robot movements
"""""""""""""""
def pickup(offset, pickup_pos, joint_vel, cart_vel, initial_placement=False):
    robot.SetConf(1,1,-1)
    hor_offset = offset
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
    robot.MoveLin(x,y,z,0,90,0)

    if initial_placement:
        robot.Delay(10)
    else:
        robot.Delay(2)

    #offset axis
    robot.MoveLin(x,hor_offset,z,0,90,0)
    robot.MoveLin(x+3,hor_offset,z,0,90,0)

    #move back up
    robot.MoveLin(x+3,hor_offset,z+30,0,90,0) 
    robot.SetJointVel(joint_vel)
    robot.MovePose(x+6,0,z+70,0,90,0)

def rotation(angle, ang_vel):
    robot.WaitIdle()
    robot_data = robot.GetRobotRtData()
    curr_joint_pos = robot_data.rt_joint_pos.data
    print(curr_joint_pos)
    robot.SetJointVel(int(ang_vel/2))
    robot.MoveJoints(*curr_joint_pos[:5],int(angle/6))
    #ser.write("R\n".encode('utf-8'))
    robot.SetJointVel(ang_vel)
    robot.MoveJoints(*curr_joint_pos[:5],angle)
    robot.MoveJoints(*curr_joint_pos[:5],0)
    robot.SetJointVel(int(ang_vel/2))

def translation(distance, lin_vel):
    #robot.WaitIdle()
    robot.SetCartLinVel(lin_vel)
    robot.MoveLinRelTRF(0,0,distance,0,0,0)
    robot.MoveLinRelTRF(0,0,-distance,0,0,0)

def helix(distance, lin_vel, angle, ang_vel):
    robot.WaitIdle()
    robot.SetCartLinVel(lin_vel)
    robot.SetJointVel(ang_vel)
    robot.MoveLinRelTRF(0,0,distance,0,0,angle)
    robot.MoveLinRelTRF(0,0,-distance,0,0,-angle)

def clear_beam():
    robot.SetCartLinVel(5)
    robot.SetConf(1,1,1)
    robot.MoveLin(70,0,350,0,90,0)

def waitTrigger(msg, data, ser):
    while data != msg:
        data = ser.readline().decode().strip()
    data = 0

def get_move_status():
    robot_status = robot.GetStatusRobot()
    return robot_status.end_of_block_status

def get_checkpoint():
    robot_data = robot.GetRobotRtData()  
    return robot_data.rt_checkpoint.data[0]

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


