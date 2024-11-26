import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

x_0 =  500
y_0 = 1000
# # Define the arc parameters
# radius = 1
# start_angle = np.pi / 4
# end_angle = 3 * np.pi / 4
L = 68 #mm
t = np.linspace(0, 7.5, 1000) #s
# Generate angles within the arc
# theta = np.linspace(start_angle, end_angle, 100)

# # Calculate the x and y coordinates of the arc
# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# Create the sinusoidal wave along the arc
ee_angle = 7
max_angle = ee_angle*2.5  #deg
frequency = 2.88  #cycles/s 
# theta = amplitude * np.sin(frequency*t - np.pi/2)   #deg
theta = max_angle*signal.sawtooth(2*np.pi*frequency*t, 0.5)
# x = L*(np.sin(amplitude*np.pi/180) - np.sin(theta*np.pi/180)) + x_0 #mm
# y = L*(np.cos(theta*np.pi/180) - np.cos(amplitude*np.pi/180)) + y_0 #mm
x = np.sin(theta*np.pi/180)
y = np.cos(theta*np.pi/180)
# Plot the sinusoidal arc
plt.plot(t, theta)
plt.plot(t, x)
plt.plot(t, y)
#plt.axis('equal')  # Equal aspect ratio
# plt.show() 
x_range = 2*L*np.sin(max_angle*np.pi/180)
y_range = L*(1-np.cos(max_angle*np.pi/180))

print("X Range: ", x_range)
print("Y Range: ", y_range)