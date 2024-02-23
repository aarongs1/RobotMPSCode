import mecademicpy.robot as mdr

robot = mdr.Robot()                     #connect to robot's ip address
robot.Connect(address='192.168.0.100')
robot.ActivateRobot()                   #activate and home robot
robot.Home()
robot.WaitHomed()
