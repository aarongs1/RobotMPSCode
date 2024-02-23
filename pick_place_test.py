import mecademicpy.robot as mdr

robot = mdr.Robot()                     #connect to robot's ip address
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()                   #activate and home robot
robot.Home()

robot.SetTrf(0,0,0,0,0,0)
robot.SetCartAngVel(5)
robot.SetCartLinVel(10)
robot.SetJointVel(1)
robot.MovePose(130,0,240,-180,0,183)
robot.MoveLin(130,0,239,-180,0,183)
robot.MoveLin(130,0,235,-180,0,183)
