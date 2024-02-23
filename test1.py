import mecademicpy.robot as mdr

robot = mdr.Robot()                     #connect to robot's ip address
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()                   #activate and home robot
robot.Home()

robot.SetCartAngVel(100)
robot.SetCartLinVel(100)
robot.SetJointVel(10)
robot.MovePose(120,0,238,-180,0,180)
robot.MovePose(120,0,200,-180,0,135)
robot.MovePose(120,0,200,-180,0,135)
robot.Delay(2)
robot.MoveLinRelWrf(0,0,0,0,0,180)
robot.MoveLinRelWrf(0,0,0,0,0,-180)
robot.Delay(1)
robot.MovePose(120,0,200,-180,-15,135)
robot.Delay(2)
robot.MoveLinRelWrf(0,0,0,0,0,180)
robot.MoveLinRelWrf(0,0,0,0,0,-180)
robot.Delay(1)
robot.MovePose(120,0,200,-180,-30,135)
robot.Delay(2)
robot.MoveLinRelWrf(0,0,0,0,0,180)
robot.MoveLinRelWrf(0,0,0,0,0,-180)
robot.Delay(1)
robot.MovePose(120,0,200,-180,-45,135)
robot.Delay(2)
robot.MoveLinRelWrf(0,0,0,0,0,180)
robot.MoveLinRelWrf(0,0,0,0,0,-180)
robot.MovePose(120,0,238,-180,0,180)

SetTrf(0,0,35,0,0,0)
SetCartAngVel(10)
SetCartLinVel(100)
SetJointVel(10)
MovePose(120,0,238,-180,0,180)
MovePose(120,0,160,-180,0,135)
MovePose(120,0,160,-180,0,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(120,0,160,-180,-15,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(120,0,160,-180,-30,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(120,0,160,-180,-45,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
MovePose(120,0,238,-180,0,180)

#for wu setup
SetTrf(0,0,35,0,0,0)
SetCartAngVel(30)
SetCartLinVel(100)
SetJointVel(10)
MovePose(80,0,238,-180,0,180)
MovePose(80,0,183,-180,0,135)
MovePose(80,0,183,-180,0,135)
Delay(5)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(80,0,183,-180,-15,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(80,0,183,-180,-30,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(80,0,183,-180,-45,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
MovePose(80,0,238,-180,0,180)

#with offset
SetTrf(0,0,35,0,0,0)
SetCartAngVel(5)
SetCartLinVel(100)
SetJointVel(10)
MovePose(80,5.5,238,-180,0,180)
MovePose(80,5.5,180,-180,0,135)
MovePose(80,5.5,180,-180,0,135)
Delay(5)
MoveLinRelWrf(0,0,0,0,0,180)
MoveLinRelWrf(0,0,0,0,0,-180)
Delay(1)
MovePose(80,5.5,180,-180,-15,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,120)
MoveLinRelWrf(0,0,0,0,0,-120)
Delay(1)
MovePose(80,5.5,180,-180,-30,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,160)
MoveLinRelWrf(0,0,0,0,0,-160)
Delay(1)
MovePose(80,5.5,180,-180,-45,135)
Delay(2)
MoveLinRelWrf(0,0,0,0,0,160)
MoveLinRelWrf(0,0,0,0,0,-160)
MovePose(80,0,238,-180,0,180)