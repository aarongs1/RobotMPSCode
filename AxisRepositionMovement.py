import mecademicpy.robot as mdr
import mecademicpy.mx_robot_def as mx_robot
import serial

robot = mdr.Robot()                     #connect to robot's ip address
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()                   #activate and home robot
robot.Home()
robot.WaitHomed()



def pickup(offset, pickup_pos, joint_vel, cart_vel, initial_placement=False):
    x, y, z = pickup_pos

    #move down
    if y > 0:
        robot.SetJointVel(joint_vel)
        robot.MovePose(x+4,y,z+70,0,90,0)
        robot.SetCartLinVel(cart_vel)
        robot.MoveLin(x+4,y,z+10,0,90,0)
        robot.SetCartLinVel(int(cart_vel/2))
        robot.MoveLin(x+4,y,z,0,90,0)
        robot.Delay(1)
    else:
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
    robot.MoveLin(x,offset,z,0,90,0)
    robot.MoveLin(x+3,offset,z,0,90,0)

    #move back up
    robot.MoveLin(x+3,offset,z+30,0,90,0)
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

def waitTrigger(msg, data, ser):
    while data != msg:
        data = ser.readline().decode().strip()
    data = 0

if __name__ == "__main__":
    program = 1

    #setup serial
    comport = 'COM7'
    baudrate = 115200
    #ser = serial.Serial(comport, baudrate, timeout=0.1)
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


