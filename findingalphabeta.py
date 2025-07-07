import numpy as np
from scipy import integrate
from math import pi
import matplotlib.pyplot as plt

# ==== パラメータ ====
J_over_I   = 0.25     # J/I
ALPHA_MAX  = 90       # α の上限 (deg)
BETA_MAX   = 90       # β の上限 (deg)
TOL        = 1e-2     # 許容誤差 (rad)
MESH_N     = 200      # θ 分割数

# ==== 数式実装 ====
def S(theta, alpha, beta):
    return -np.sqrt(2)*(np.cos(alpha)*np.sin(beta)
                        + np.sin(alpha)*np.cos(beta)*np.cos(theta))*np.sin(beta)

def T(theta, alpha, beta):
    return np.cos(alpha)*np.cos(beta) - np.sin(alpha)*np.sin(beta)*np.cos(theta)

def dpsi_dtheta(theta, alpha, beta, J_over_I):
    t = T(theta, alpha, beta)
    denom = (t - 1) * (1 - t + J_over_I * (1 + t)) * np.sqrt(1 + t)
    return (J_over_I * S(theta, alpha, beta)) / denom

def psi_2pi(alpha, beta, J_over_I):
    thetas = np.linspace(0.0, 2.0 * pi, MESH_N + 1)
    return integrate.trapezoid(dpsi_dtheta(thetas, alpha, beta, J_over_I), thetas)

# ==== 総当たり探索 ====
solutions = []
solutions2 = []
x_vals = []
y_vals = []
x_vals2 = []
y_vals2 = []

for a_deg in range(ALPHA_MAX + 1):
    alpha = np.deg2rad(a_deg)
    for b_deg in range(BETA_MAX + 1):
        beta = np.deg2rad(b_deg)
        psi_val = psi_2pi(alpha, beta, 0.2)
        psi_val2 = psi_2pi(alpha, beta, 0.3)

        if abs(psi_val - pi) < TOL:
            solutions.append((a_deg, b_deg, psi_val))
            x_vals.append(b_deg - a_deg)
            y_vals.append(b_deg + a_deg)

        if abs(psi_val2 - pi) < TOL:
            solutions2.append((a_deg, b_deg, psi_val2))
            x_vals2.append(b_deg - a_deg)
            y_vals2.append(b_deg + a_deg)

    print(f'α = {a_deg:2d}° まで探索終了')

# ==== 結果表示 ====
print('\n=== ψ(2π) ? +π となる (α, β) 一覧 (deg,deg) ===')
if solutions:
    for a_deg, b_deg, psi_val in solutions:
        err = psi_val - pi
        print(f'α={a_deg:3d}°, β={b_deg:3d}°  (誤差 {err:+.3e} rad)')
else:
    print('見つからなかったよ…')

if solutions2:
    for a_deg, b_deg, psi_val2 in solutions2:
        err = psi_val2 - pi
        print(f'α={a_deg:3d}°, β={b_deg:3d}°  (誤差 {err:+.3e} rad)')

# ==== グラフ表示 ====
plt.figure(figsize=(6, 6))
plt.scatter(x_vals, y_vals, color='blue', label='J/I = 0.2')
plt.scatter(x_vals2, y_vals2, color='red', label='J/I = 0.3')
plt.title('ψ(2π) ? +π (x=β?α, y=β+α)')
plt.xlabel('β ? α [deg]')
plt.ylabel('β + α [deg]')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()