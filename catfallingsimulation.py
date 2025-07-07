from vpython import canvas, vector, cone, sphere, cylinder, box, color, rate, rotate
import numpy as np
import time
# === パラメータ ===

z_start  = 9.0
g        = 5.0
dt       = 0.001
omega    = np.pi

# === 身長と体重から猫ひねりするための曲げ角度(a)を計算 ===

height = float(input("身長は何mですか？: "))
mass  = float(input("体重は何kgですか？: "))

bsa = 0.1 * mass ** (2/3) * 0.8 #BSAの計算 BSA=2πrh + 2πr^2から,r^2+hr-BSA/(2π)=0の二次方程式

a = 1.0
b = height
c = - bsa / (2 * np.pi)

disc = b ** 2 - 4 * a * c
if disc < 0:
    raise ValueError("計算がおかしいよ")

r = (-b + np.sqrt(disc)) / (2 * a)

print(f"半径 = {r * 100:.2f} cm")

# === 身長と求めた半径から猫ひねり率=0.5ができるθを計算 ===

half = height / 2

gamma = half ** 2 / (6 * r ** 2) - 0.5     #係数 γ

def f(theta):
    """方程式 f(θ)=0 の形に整形"""
    return np.cos(theta) / (1 + gamma * np.sin(theta) ** 2) - 0.5

# 2 分法で根を探す（0 < θ < π の範囲に 1 つだけ存在）
a, b = 0.0, np.pi        # 区間
fa, fb = f(a), f(b)
if fa * fb > 0:
    raise ValueError("区間 (0, π) に根が見つかりません")

for _ in range(100):     # 収束するまで最大 100 iter
    mid = (a + b) / 2
    fm  = f(mid)
    if fa * fm <= 0:     # 根は [a, mid] 側
        b, fb = mid, fm
    else:                # 根は [mid, b] 側
        a, fa = mid, fm
    if abs(b - a) < 1e-10:
        break

theta = (a + b) / 2      # [rad]
print(f" θ = {np.degrees(theta):.2f}°")

# === 特定の高さから自由落下をしつつ猫ひねりをするシミュレーション ===

# キャンバスと床
scene = canvas(width=1000, height=600,
               center=vector(0, 0, 1),
               background=color.white)

floor = box(pos=vector(0, 0, -half * 0.75),
            size=vector(4, 4, 0.02),
            color=color.gray(0.9), opacity=0.3)

# 猫の初期状態
front = cylinder(pos=vector(0, 0, z_start),
                 axis=vector(half, 0, 0),
                 radius=r,
                 color=color.orange)
frontleg = cylinder(pos=vector(half * 0.75, r/2, z_start),
                 axis=vector(0, 0, half / 2),
                 radius=r * 0.3,
                 color=color.orange)
frontleg2 = cylinder(pos=vector(half * 0.75, -r/2, z_start),
                 axis=vector(0, 0, half / 2),
                 radius=r * 0.3,
                 color=color.orange)
back = cylinder(pos=vector(0, 0, z_start),
                 axis=vector(-half, 0, 0),
                 radius=r,
                 color=color.blue)
backleg = cylinder(pos=vector(-half * 0.75, r/2, z_start),
                 axis=vector(0, 0, half / 2),
                 radius=r * 0.3,
                 color=color.blue)
backleg2 = cylinder(pos=vector(-half * 0.75, -r/2, z_start),
                 axis=vector(0, 0, half / 2),
                 radius=r * 0.3,
                 color=color.blue)

head = sphere(pos=vector(half + r * 1.5, 0, z_start), radius= r * 1.5, color=color.red)

tail = cylinder(pos=vector(-half, 0, z_start),
                 axis=vector(0, 0, -half),
                 radius=r * 0.3,
                 color=color.red)

ear =  cone(pos=vector(half + r, r / np.sqrt(2), - r * 1.5 / np.sqrt(2) + z_start), axis=vector(0, r, -r), radius=r, color=color.green)
ear2 =  cone(pos=vector(half + r, -r / np.sqrt(2), - r * 1.5 / np.sqrt(2) + z_start), axis=vector(0, r, -r), radius=r, color=color.green)


#高さごとの動き
while True:
    z = z_start
    v = 0.0
    t = 0.0
    thetanow = 0.0
    omeganow = 0.0

    while z > 0:
        rate(1/dt)
        #time.sleep(10)

        if z > (9 / 10) * z_start:

            thetanow = (-10 * theta / z_start) * z + 10 * theta
            front.pos.z = back.pos.z = z
            front.axis = vector(half * np.cos(thetanow), 0, half * np.sin(thetanow))
            back.axis = vector(-half * np.cos(thetanow), 0, half * np.sin(thetanow))
            frontleg.pos = front.axis * 0.75 + vector(0,r/2,z)
            frontleg2.pos = front.axis * 0.75 + vector(0,-r/2,z)
            frontleg.axis = vector(half/2 * np.cos(thetanow + np.pi / 2),0,half/2 * np.sin(thetanow + np.pi / 2))
            frontleg2.axis = vector(half/2 * np.cos(thetanow + np.pi / 2),0,half/2 * np.sin(thetanow + np.pi / 2))
            backleg.pos = back.axis * 0.75 + vector(0,r/2,z)
            backleg2.pos = back.axis * 0.75 + vector(0,-r/2,z)
            backleg.axis = vector(-half/2 * np.cos(thetanow + np.pi / 2),0,half/2 * np.sin(thetanow + np.pi / 2))
            backleg2.axis = vector(-half/2 * np.cos(thetanow + np.pi / 2),0,half/2 * np.sin(thetanow + np.pi / 2))
            head.pos = front.axis + vector(r * 1.5 * np.cos(thetanow),0,z + r * 1.5 * np.sin(thetanow))
            tail.pos = back.axis + vector(0,0,z)
            tail.axis = vector(half * np.cos(thetanow + np.pi / 2),0,-half * np.sin(thetanow + np.pi / 2))
            ear.pos = head.pos + vector(np.sin(thetanow),1,-np.cos(thetanow)) * r / np.sqrt(2)
            ear2.pos = head.pos + vector(np.sin(thetanow),-1,-np.cos(thetanow)) * r / np.sqrt(2)
            ear.axis = vector(np.sin(thetanow),1,-np.cos(thetanow)) * r
            ear2.axis = vector(np.sin(thetanow),-1,-np.cos(thetanow)) * r
        elif z > (2 / 10) * z_start:

            omeganow = (-10 * omega / (7 * z_start)) * z + 9 / 7 * omega
            front.pos.z = back.pos.z = z
            front.axis = vector(half * np.cos(theta), half * np.sin(theta) * np.sin(-omeganow), half * np.sin(theta) * np.cos(-omeganow))
            back.axis = vector(-half * np.cos(theta), half * np.sin(theta) * np.sin(-omeganow), half * np.sin(theta) * np.cos(-omeganow))
            head.pos = front.pos + front.axis * (r * 1.5 + half) / half
            frontleg.pos = front.pos + front.axis * 0.75 + vector(0, r/2 * np.cos(omeganow), -r/2 * np.sin(omeganow))
            frontleg2.pos = front.pos + front.axis * 0.75 + vector(0, -r/2 * np.cos(omeganow), r/2 * np.sin(omeganow))
            frontleg.axis = frontleg2.axis =  half / 2 * vector(-np.sin(theta) * np.cos(2 * omeganow),
                                                                 np.cos(omeganow) * np.sin(2 * omeganow) - np.sin(omeganow) * np.cos(theta) * np.cos(2 * omeganow),
                                                                 np.sin(omeganow) * np.sin(2 * omeganow) + np.cos(omeganow) * np.cos(theta) * np.cos(2 * omeganow))
            backleg.pos = back.pos + back.axis * 0.75 + vector(0, r/2 * np.cos(omeganow), -r/2 * np.sin(omeganow))
            backleg2.pos = back.pos + back.axis * 0.75 + vector(0, -r/2 * np.cos(omeganow), r/2 * np.sin(omeganow))
            backleg.axis = backleg2.axis =  half / 2 * vector(np.sin(theta) * np.cos(2 * omeganow),
                                                                 np.cos(omeganow) * np.sin(2 * omeganow) - np.sin(omeganow) * np.cos(theta) * np.cos(2 * omeganow),
                                                                 np.sin(omeganow) * np.sin(2 * omeganow) + np.cos(omeganow) * np.cos(theta) * np.cos(2 * omeganow))
            tail.pos = back.axis + back.pos
            tail.axis = -half * vector(np.sin(theta) * np.cos(2 * omeganow),
                                       np.cos(omeganow) * np.sin(2 * omeganow) - np.sin(omeganow) * np.cos(theta) * np.cos(2 * omeganow),
                                       np.sin(omeganow) * np.sin(2 * omeganow) + np.cos(omeganow) * np.cos(theta) * np.cos(2 * omeganow))

            base = r / np.sqrt(2)
            n_axis = vector(np.cos(theta), 0, np.sin(theta))

            earL0 = vector( base * np.sin(theta),  base * np.sqrt(2), -base * np.cos(theta))  # 上耳
            earR0 = vector( base * np.sin(theta), -base * np.sqrt(2), -base * np.cos(theta))  # 下耳

            earL_rot = rotate(earL0, angle=-2*omeganow, axis=n_axis)
            earL_rot = rotate(earL_rot, angle=omeganow, axis=vector(1, 0, 0))

            earR_rot = rotate(earR0, angle=-2*omeganow, axis=n_axis)
            earR_rot = rotate(earR_rot, angle=omeganow, axis=vector(1, 0, 0))

            ear.pos  = head.pos + earL_rot
            ear.axis = earL_rot
            ear2.pos = head.pos + earR_rot
            ear2.axis = earR_rot

        elif z >= (1 / 10) * z_start:

            thetanow = (10 * theta / z_start) * z - theta

            front.pos.z = back.pos.z = z
            front.axis = vector(half * np.cos(thetanow), 0, -half * np.sin(thetanow))
            back.axis = vector(-half * np.cos(thetanow), 0, -half * np.sin(thetanow))
            frontleg.pos = front.axis * 0.75 + vector(0,-r/2,z)
            frontleg2.pos = front.axis * 0.75 + vector(0,r/2,z)
            frontleg.axis = vector(half/2 * np.cos(thetanow + np.pi / 2),0,-half/2 * np.sin(thetanow + np.pi / 2))
            frontleg2.axis = vector(half/2 * np.cos(thetanow + np.pi / 2),0,-half/2 * np.sin(thetanow + np.pi / 2))
            backleg.pos = back.axis * 0.75 + vector(0,-r/2,z)
            backleg2.pos = back.axis * 0.75 + vector(0,r/2,z)
            backleg.axis = vector(-half/2 * np.cos(thetanow + np.pi / 2),0,-half/2 * np.sin(thetanow + np.pi / 2))
            backleg2.axis = vector(-half/2 * np.cos(thetanow + np.pi / 2),0,-half/2 * np.sin(thetanow + np.pi / 2))
            head.pos = front.axis + vector(r * 1.5 * np.cos(thetanow),0,z - r * 1.5 * np.sin(thetanow))
            tail.pos = back.axis + vector(0,0,z)
            tail.axis = vector(half * np.cos(thetanow + np.pi / 2),0,half * np.sin(thetanow + np.pi / 2))
            ear.pos = head.pos + vector(np.sin(thetanow),-1,np.cos(thetanow)) * r / np.sqrt(2)
            ear2.pos = head.pos + vector(np.sin(thetanow),1,np.cos(thetanow)) * r / np.sqrt(2)
            ear.axis = vector(np.sin(thetanow),1,np.cos(thetanow)) * r
            ear2.axis = vector(np.sin(thetanow),-1,np.cos(thetanow)) * r

        else:
            front.pos.z = back.pos.z = z
            front.axis = vector(half, 0, 0)
            back.axis = vector(-half, 0, 0)
            frontleg.pos = front.axis * 0.75 + vector(0,-r/2,z)
            frontleg2.pos = front.axis * 0.75 + vector(0,r/2,z)
            frontleg.axis = vector(0,0,-half/2)
            frontleg2.axis = vector(0,0,-half/2)
            backleg.pos = back.axis * 0.75 + vector(0,-r/2,z)
            backleg2.pos = back.axis * 0.75 + vector(0,r/2,z)
            backleg.axis = vector(0,0,-half/2)
            backleg2.axis = vector(0,0,-half/2)
            head.pos = front.axis + vector(r * 1.5,0,z)
            tail.pos = back.axis + vector(0,0,z)
            tail.axis = vector(0,0,half)
            ear.pos = head.pos + vector(0,-1,1) * r / np.sqrt(2)
            ear2.pos = head.pos + vector(0,1,1) * r / np.sqrt(2)
            ear.axis = vector(0,-1,1) * r
            ear2.axis = vector(0,1,1) * r

        v -= g * dt
        z += v * dt

        if z < 0:
            z = 0
        t += dt

        #print(f"t = {t:.2f}")
