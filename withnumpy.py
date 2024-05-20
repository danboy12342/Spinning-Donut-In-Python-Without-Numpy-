import numpy as np
import math
import time

screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.02
illumination = ".,-~:;=!*#$@"

A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))

def render_frame(A, B):
    cos_A, sin_A = np.cos(A), np.sin(A)
    cos_B, sin_B = np.cos(B), np.sin(B)

    output = np.full((screen_size, screen_size), ' ')
    zbuffer = np.zeros((screen_size, screen_size))

    phi = np.arange(0, 2 * np.pi, phi_spacing)
    theta = np.arange(0, 2 * np.pi, theta_spacing)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    circle_x = R2 + R1 * cos_theta[:, np.newaxis]
    circle_y = R1 * sin_theta[:, np.newaxis]

    x = (cos_B * cos_phi + sin_A * sin_B * sin_phi) * circle_x - cos_A * sin_B * circle_y
    y = (sin_B * cos_phi - sin_A * cos_B * sin_phi) * circle_x + cos_A * cos_B * circle_y
    z = K2 + cos_A * sin_phi * circle_x + sin_A * circle_y

    ooz = np.where(z != 0, 1 / z, 0)
    xp = np.clip((screen_size / 2 + K1 * ooz * x).astype(int), 0, screen_size - 1)
    yp = np.clip((screen_size / 2 - K1 * ooz * y).astype(int), 0, screen_size - 1)

    L1 = cos_phi * cos_theta[:, np.newaxis] * sin_B
    L2 = cos_A * sin_phi * cos_theta[:, np.newaxis]
    L3 = sin_A * sin_theta[:, np.newaxis]
    L4 = cos_B * (cos_A * sin_theta[:, np.newaxis] - sin_phi * cos_theta[:, np.newaxis] * sin_A)
    L = L1 - L2 - L3 + L4

    mask_L = L > 0
    L_index = np.round(L * 8).astype(int)
    L_index = np.clip(L_index, 0, len(illumination) - 1)

    for i in range(len(theta)):
        for j in range(len(phi)):
            if mask_L[i, j] and ooz[i, j] > zbuffer[xp[i, j], yp[i, j]]:
                zbuffer[xp[i, j], yp[i, j]] = ooz[i, j]
                output[xp[i, j], yp[i, j]] = illumination[L_index[i, j]]

    return output

def pprint(array):
    for row in array:
        print("".join(row))

if __name__ == "__main__":
    while True:
        A += theta_spacing
        B += phi_spacing
        print("\x1b[H")
        pprint(render_frame(A, B))
        time.sleep(0.03)
