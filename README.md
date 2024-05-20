# Spinning-Donut-In-Python-Without-Numpy-
### the idea is to explain the usefulness of numpy buy doing something without numpy and then seeing what the numpy functions are doing, but i'm not gonna help you with that, figure out the learning yourself

* written in python using the math and time library
*no other dependance for the "main.py" file

### *how it works*

We replace the Numpy Array Initialization, Trigonometric Calculations and Element-Wise operations.


1. **Initialization**:
    ```python
    output = np.full((screen_size, screen_size), ' ')
    zbuffer = np.zeros((screen_size, screen_size))
    ```

2. **Creating Arrays for `phi` and `theta`**:
    ```python
    phi = np.arange(0, 2 * np.pi, phi_spacing)
    theta = np.arange(0, 2 * np.pi, theta_spacing)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    ```

3. **Computing Circle Coordinates and Transformations**:
    ```python
    circle_x = R2 + R1 * cos_theta[:, np.newaxis]
    circle_y = R1 * sin_theta[:, np.newaxis]

    x = (cos_B * cos_phi + sin_A * sin_B * sin_phi) * circle_x - cos_A * sin_B * circle_y
    y = (sin_B * cos_phi - sin_A * cos_B * sin_phi) * circle_x + cos_A * cos_B * circle_y
    z = K2 + cos_A * sin_phi * circle_x + sin_A * circle_y
    ```

4. **Handling Division and Clipping**:
    ```python
    ooz = np.where(z != 0, 1 / z, 0)
    xp = np.clip((screen_size / 2 + K1 * ooz * x).astype(int), 0, screen_size - 1)
    yp = np.clip((screen_size / 2 - K1 * ooz * y).astype(int), 0, screen_size - 1)
    ```

5. **Calculating Illumination and Mask**:
    ```python
    L1 = cos_phi * cos_theta[:, np.newaxis] * sin_B
    L2 = cos_A * sin_phi * cos_theta[:, np.newaxis]
    L3 = sin_A * sin_theta[:, np.newaxis]
    L4 = cos_B * (cos_A * sin_theta[:, np.newaxis] - sin_phi * cos_theta[:, np.newaxis] * sin_A)
    L = L1 - L2 - L3 + L4

    mask_L = L > 0
    L_index = np.round(L * 8).astype(int)
    L_index = np.clip(L_index, 0, len(illumination) - 1)
    ```
by using numpy this code would be far more effeciant and by having a look at both you should learn that quite quickly, at least thats the idea.


### how we do away with numpy

and how we actually get a donut to spin in our terminal, these pricables apply to all versions of this fairly popular early project

### Constants and Initial Variables

```python
import math
import time

screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.02
illumination = ".,-~:;=!*#$@"
```

- math: Provides mathematical functions, such as trigonometry.
- time: Allows for creating delays.
- screen_size: The size of the output screen, 40x40 characters.
- theta_spacing & phi_spacing: Angles in radians used to iterate through the surface of the torus.
- illumination: A string of characters used to represent different levels of illumination.

```python
A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))
```

- `A` and `B`: Rotation angles around the X-axis and Z-axis respectively.
- `R1`, `R2`: Radii of the torus (donut).
- `K2`: A scaling factor for z-coordinates.
- `K1`: A scaling factor for projection calculations, dependent on screen size and torus radii.

### Function `render_frame`

This function calculates and returns the current frame of the rotating donut as a 2D list of characters.

```python
def render_frame(A, B):
    cos_A, sin_A = math.cos(A), math.sin(A)
    cos_B, sin_B = math.cos(B), math.sin(B)

    output = [[" " for _ in range(screen_size)] for _ in range(screen_size)]
    zbuffer = [[0 for _ in range(screen_size)] for _ in range(screen_size)]
```

- `cos_A`, `sin_A`, `cos_B`, `sin_B`: Pre-compute the sine and cosine values for angles `A` and `B`.
- `output`: A 2D list initialized with spaces to represent the screen.
- `zbuffer`: A 2D list initialized with zeros to store the z-depth of each screen pixel.

```python
    for phi in range(0, int(2 * math.pi / phi_spacing)):
        cos_phi = math.cos(phi * phi_spacing)
        sin_phi = math.sin(phi * phi_spacing)
        
        for theta in range(0, int(2 * math.pi / theta_spacing)):
            cos_theta = math.cos(theta * theta_spacing)
            sin_theta = math.sin(theta * theta_spacing)

            circle_x = R2 + R1 * cos_theta
            circle_y = R1 * sin_theta
```

- The outer loop iterates over `phi`, the angle around the torus' cross-section.
- The inner loop iterates over `theta`, the angle around the torus' central axis.
- `cos_phi`, `sin_phi`, `cos_theta`, `sin_theta`: Pre-compute sine and cosine values for the current angles.
- `circle_x`, `circle_y`: Calculate the coordinates of a point on the torus' surface in its local 2D plane.

```python
            x = (cos_B * cos_phi + sin_A * sin_B * sin_phi) * circle_x - cos_A * sin_B * circle_y
            y = (sin_B * cos_phi - sin_A * cos_B * sin_phi) * circle_x + cos_A * cos_B * circle_y
            z = K2 + cos_A * sin_phi * circle_x + sin_A * circle_y
```

- Transform the 2D local coordinates (`circle_x`, `circle_y`) into 3D space, considering rotations by `A` and `B`.

```python
            ooz = 1 / z if z != 0 else 0
            xp = int(screen_size / 2 + K1 * ooz * x)
            yp = int(screen_size / 2 - K1 * ooz * y)
```

- `ooz`: One over the z-coordinate for perspective division.
- `xp`, `yp`: Project the 3D coordinates onto the 2D screen.

```python
            L = cos_phi * cos_theta * sin_B - cos_A * sin_phi * cos_theta - sin_A * sin_theta + cos_B * (cos_A * sin_theta - sin_phi * cos_theta * sin_A)
```

- `L`: Calculate the illumination factor using the normal vector of the torus' surface at the point. This determines the shading of the point.

```python
            if L > 0:
                L_index = int(round(L * 8))
                if L_index >= 0 and L_index < len(illumination):
                    if ooz > zbuffer[xp][yp]:
                        zbuffer[xp][yp] = ooz
                        output[xp][yp] = illumination[L_index]
```

- If L is positive, determine the corresponding character from the `illumination` string.
- Update the `zbuffer` and `output` only if the current point is closer to the viewer than previous points (`ooz > zbuffer[xp][yp]`).

### Main Loop

This loop continuously updates the rotation angles `A` and `B`, generates and prints the frames, and adds a delay to create the animation.

```python
if __name__ == "__main__":
    while True:
        A += theta_spacing
        B += phi_spacing
        print("\x1b[H")  # Escape sequence to move the cursor to the top-left corner of the terminal
        pprint(render_frame(A, B))
        time.sleep(0.03)  # Add a small delay to make the animation smoother
````

- `A` and `B` are incremented to simulate rotation.
- `render_frame(A, B)``` generates the next frame.
- pprint prints the frame.                        
- `time.sleep(0.03)` adds a delay to control the animation speed.
