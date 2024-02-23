import mecademicpy.robot as mdr

robot = mdr.Robot()                     #connect to robot's ip address
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()                   #activate and home robot
robot.Home()

SetTrf(0,0,35,0,0,0)
SetCartAngVel(100)
SetCartLinVel(100)
SetJointVel(10)
MovePose(156,1,238,-180,0,180)
MovePose(156,1,175.5,-180,0,135)
MovePose(156,1,175.5,-180,0,135)
Delay(2)
MovePose(156,1,175.5,-180,10,-45)
MovePose(156,1,175.5,-180,10,135)
Delay(1)
MovePose(156,1,175.5,-180,20,135)
Delay(2)
MovePose(156,1,175.5,-180,20,-45)
MovePose(156,1,175.5,-180,20,135)
Delay(1)
MovePose(156,1,175.5,-180,30,135)
Delay(2)
MovePose(156,1,175.5,-180,30,-45)
MovePose(156,1,175.5,-180,30,135)
Delay(1)
MovePose(156,1,175.5,-180,40,135)
Delay(2)
MovePose(156,1,175.5,-180,40,-45)
MovePose(156,1,175.5,-180,40,135)
Delay(1)
MovePose(156,1,175.5,-180,50,135)
Delay(2)
MovePose(156,1,175.5,-180,50,-45)
MovePose(156,1,175.5,-180,50,135)
MovePose(156,1,238,-180,0,180)
