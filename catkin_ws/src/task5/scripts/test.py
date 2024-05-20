import numpy as np
import math

hola_theta, hola_x, hola_y = 0, 0, 0

print("Initial location: " + str(hola_x) + "," +  str(hola_y) + "," + str(hola_theta))

x, y, theta_d = 500, 500, 0

print("Desired location: " + str(x)  + "," + str(y)  + "," + str(theta_d))

ct = hola_theta
x0, y0 = hola_x, hola_y
diff = math.dist([hola_x, hola_y],[x, y])
print("Diff: " + str(diff))

#diff = 707.106
c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
theta = math.atan2( c[1], c[0])

kp = 500*1.414
speed = 1
diff = 1
vx = kp*math.cos(theta)*diff
vy = kp*math.sin(theta)*diff
omega = kp*speed*(theta_d - ct)
print("Vx :" + str(vx) + " Vy :" + str(vy) + " w :" + str(omega))

#vx , vy, omega = 0, 0, 3.14/2

l = 0.17483

mat = [[0, -1, l],
	   [math.sin(-60), 0.5, l],
	   [math.sin(60), 0.5, l]]

res = np.matmul(mat, [-vy, -vx, -omega])

print(res)