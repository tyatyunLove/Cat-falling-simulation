import numpy as np
from scipy import integrate
from math import pi
import matplotlib.pyplot as plt

def turningratio(theta,height,radius):

    half = height / 2
    gamma = half ** 2 / (6 * radius ** 2) - 0.5     #係数 γ
    return 1 - np.cos(theta) / (1 + gamma * np.sin(theta) ** 2)

x_vals = []
y_vals = []
x_vals2 = []
y_vals2 = []
x_vals3 = []
y_vals3 = []

for theta in range(91):
    theta1 = np.deg2rad(theta)
    rt = turningratio(theta1,1,0.1)
    x_vals.append(theta)
    y_vals.append(rt)
    rt2 = turningratio(theta1,1,0.2)
    x_vals2.append(theta)
    y_vals2.append(rt2)
    rt3 = turningratio(theta1,1,0.3)
    x_vals3.append(theta)
    y_vals3.append(rt3)

print(f'計算を完了しました')

plt.figure(figsize=(6,6))
plt.scatter(x_vals, y_vals, color='blue')
plt.scatter(x_vals2, y_vals2, color='red')
plt.scatter(x_vals3, y_vals3, color='green')
plt.title('rate of twist and bending angle')
plt.xlabel('Bending angle[deg]')
plt.ylabel('Rate of twist')
plt.grid(True)
plt.tight_layout()
plt.show()