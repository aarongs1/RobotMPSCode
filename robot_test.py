import mecademicpy.robot as mdr

robot = mdr.Robot()                     #connect to robot's ip address
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()                   #activate and home robot
robot.Home()

robot.MovePose(170,0,180,0,180,0)   #move to initial position
for i in range(5):                  #pick up next mouse
    xpos = -80 + 40*i
    robot.MovePose(xpos,-150,180,0,180,0)  #move to initial pick up position
    robot.MovePose(xpos,-150,120,0,180,0)    #move down to pick up mouse
    robot.MovePose(xpos,-150,180,0,180,0)  #move back to initial pick up position
    robot.MovePose(170,0,180,0,90,0)   #move to starting position

    robot.MovePose(170,0,180,0,90,20)  #do necessary rotations for therapy
    robot.MovePose(170,0,180,0,90,40)
    robot.MovePose(170,0,180,0,90,60)
    robot.MovePose(170,0,180,0,90,40)
    robot.MovePose(170,0,180,0,90,20)
    robot.MovePose(170,0,180,0,90,0)

    robot.MovePose(170,0,180,0,180,0)   #move back to starting position



#pick up
MovePose(130.2,-0.5,200,0,180,-4)
SetCartLinVel(50)
MoveLin(130.2,-0.5,130,0,180,-4)
SetCartLinVel(20)
MoveLin(130.2,-0.5,120,0,180,-4)
SetCartLinVel(5)
MoveLin(130.2,-0.5,118.5,0,180,-4)
SetCartLinVel(50)
MoveLin(130.2,-0.5,200,0,180,-4)
delay(2)
#place
SetCartLinVel(50)
MoveLin(130.2,-0.5,130,0,180,-4)
SetCartLinVel(20)
MoveLin(130.2,-0.5,120,0,180,-4)
SetCartLinVel(5)
MoveLin(130.2,-0.5,118.5,0,180,-4)
delay(5)
SetCartLinVel(50)
MoveLin(130.2,-0.5,200,0,180,-4)


#test 1   (rotating about vertical axis)
SetCartAngVel(100)
SetCartLinVel(100)
SetJointVel(10)
MovePose(120,0,238,-180,0,180)
MovePose(120,0,200,-180,0,135)
MovePose(120,0,200,-180,0,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(120,0,200,-180,-15,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(120,0,200,-180,-30,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(120,0,200,-180,-45,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)


SetTrf(0,0,0,0,0,0)
SetCartAngVel(5)
SetCartLinVel(10)
SetJointVel(10)
MovePose(130.5,0,250,-180,0,177)
//MoveLinRelWrf(0,0,0,0,0,3)

#slow test discrete angles
SetTrf(0,0,28.6,0,0,0)
MovePose(160,0.1,176,-180,0,45)
MovePose(160,0.1,176,-180,0,45)

#fast test
SetJointVel(100)
SetTrf(0,0,0,0,0,0)
MovePose(200,0.1,231,-180,0,0)
MoveJoints(0.029,45.566,-62.601,0,107.035,20000)
MoveJoints(0.029,45.566,-62.601,0,107.035,0)

#rotation test without gears
SetJointVel(10)
SetTrf(0,0,0,0,0,0)
MovePose(220,0,130,0,90,45)
//SetJointVel(100)
//MoveJoints(0,39.384,37.428,0,-77.262,20000)
//MoveJoints(0,39.384,37.428,0,-77.262,0)

#rotation test with pla gears
SetJointVel(10)
SetTrf(0,0,0,0,0,0)
MovePose(165,0,160,0,90,0)
SetJointVel(100)
MoveJoints(0,12.231,63.503,0,-75.734,20000)
MoveJoints(0,12.231,63.503,0,-75.734,0)

#rotation test with formlabs gears
SetJointVel(10)
SetTrf(0,0,0,0,0,0)
MovePose(185,0,160,0,90,0)
SetJointVel(100)
MoveJoints(0,18.453,54.079,0,-72.531,20000)
MoveJoints(0,18.453,54.079,0,-72.531,0)


#test with offset axis
SetJointVel(10)
MoveJoints(3.180,10.649,65.730,3.272,-76.400,0)
SetJointVel(50)
MoveJoints(3.180,10.649,65.730,3.272,-76.400,4000)
SetJointVel(100)
MoveJoints(3.180,10.649,65.730,3.272,-76.400,10000)
MoveJoints(3.180,10.649,65.730,3.272,-76.400,0)
