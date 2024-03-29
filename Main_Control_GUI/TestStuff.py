import matplotlib.pyplot as plt
import numpy as np

num_points = 5
angle_range = 28.78 - 5.59
r = 740.74
points_x = [158]
points_y = [110.5]
if num_points:
    interval = angle_range/(num_points-1)
    for i in range(num_points-1):
        angle_rad = (5.59 + (i+1)*interval)*np.pi/180
        points_x.append(r*np.cos(angle_rad) - 579.22)
        points_y.append(38.33 + r*np.sin(angle_rad))

plt.plot(points_x, points_y, 'o')
plt.xlim((0,160))
plt.ylim((0,400))
plt.show()