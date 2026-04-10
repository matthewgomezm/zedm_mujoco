import pandas as pd
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt

## rangefinder plotting below
df = pd.read_csv('rangefinder_data.csv')

x = df['Point_X (m)'].values
y = df['Point_Y (m)'].values
z = df['Point_Z (m)'].values
depth = df['Depth (planar)'].values

points_array = np.column_stack((x, y, z))

valid_mask = (depth > 0) & (depth <= 10.0)
valid_points = points_array[valid_mask]
valid_depths = depth[valid_mask]

if len(valid_points) > 0:
    point_cloud = pv.PolyData(valid_points)

    plotter = pv.Plotter(title="3D Vision")
    plotter.add_mesh(point_cloud,
                     scalars=valid_depths,
                     cmap="viridis",
                     point_size=15.0,
                     render_points_as_spheres=True)
    plotter.show_grid()
    plotter.add_axes()
    plotter.show()
else:
    print("no values allowed")


## imu plotting below
imu_sources = [
    ("gyro_data.csv", "Gyroscope", "rad/s", ["Gyro_X", "Gyro_Y", "Gyro_Z"]),
    ("accel_data.csv", "Accelerometer", "m/s²", ["Accel_X", "Accel_Y", "Accel_Z"]),
]

fig, axes = plt.subplots(len(imu_sources), 1, figsize=(10, 8), sharex=True)
for ax, (csv_file, title, unit, cols) in zip(axes, imu_sources):
    imu_df = pd.read_csv(csv_file)
    for col, color in zip(cols, ["r", "g", "b"]):
        ax.plot(imu_df[col], label=col, color=color)
    ax.set_title(title)
    ax.set_ylabel(unit)
    ax.legend()
    ax.grid(True)

axes[-1].set_xlabel("Time Step")
plt.tight_layout()
plt.show()